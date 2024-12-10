import numpy as np
from tritonclient.http import InferenceServerClient, InferInput, InferRequestedOutput
from tritonclient.utils import np_to_triton_dtype


def call_triton_ensemble(text: str):
    client = InferenceServerClient(url="0.0.0.0:8500")
    text = np.array([text.encode("utf-8")], dtype=object)

    input_text = InferInput(
        name="TEXTS", shape=text.shape, datatype=np_to_triton_dtype(text.dtype)
    )
    input_text.set_data_from_numpy(text, binary_data=True)

    # Вызов Triton
    response = client.infer(
        "ensemble",
        [input_text],
        outputs=[
            InferRequestedOutput("EMBEDDINGS-ONNX"),
            InferRequestedOutput("EMBEDDINGS-TRT-FP16"),
            InferRequestedOutput("EMBEDDINGS-TRT-FP32"),
            InferRequestedOutput("EMBEDDINGS-TRT-INT8"),
            InferRequestedOutput("EMBEDDINGS-TRT-BEST"),
        ],
    )

    # Возврат эмбеддингов
    return (
        response.as_numpy("EMBEDDINGS-ONNX"),
        response.as_numpy("EMBEDDINGS-TRT-FP16"),
        response.as_numpy("EMBEDDINGS-TRT-FP32"),
        response.as_numpy("EMBEDDINGS-TRT-INT8"),
        response.as_numpy("EMBEDDINGS-TRT-BEST"),
    )


def check_quality(text: str):
    embeddings_onnx, embeddings_fp16, embeddings_fp32, embeddings_int8, embeddings_best = call_triton_ensemble(text)

    def calculate_deviation(embeddings_trt, embeddings_onnx):
        return np.linalg.norm(embeddings_trt - embeddings_onnx)

    deviations = {
        "FP16": calculate_deviation(embeddings_fp16, embeddings_onnx),
        "FP32": calculate_deviation(embeddings_fp32, embeddings_onnx),
        "INT8": calculate_deviation(embeddings_int8, embeddings_onnx),
        "BEST": calculate_deviation(embeddings_best, embeddings_onnx),
    }

    return deviations


def main():
    texts = [
        "Один два три",
        "Четыре шесть семь",
        "Этот текст проверяет отклонения",
        "Тестирование ансамбля в тритончике",
        "Надеюсь, прокатит"
    ]

    # Словарь для хранения отклонений
    all_deviations = {
        "FP16": [],
        "FP32": [],
        "INT8": [],
        "BEST": [],
    }

    # Обработка каждого текста
    for text in texts:
        deviations = check_quality(text)
        for key, value in deviations.items():
            all_deviations[key].append(value)

    # Усреднение отклонений
    average_deviations = {key: np.mean(values) for key, values in all_deviations.items()}

    # Вывод результатов
    print("Усредненные отклонения TensorRT эмбеддингов от ONNX эмбеддинга:")
    for precision, deviation in average_deviations.items():
        print(f"{precision}: {deviation:.6f}")


if __name__ == "__main__":
    main()
