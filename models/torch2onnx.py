import torch
import numpy as np
import onnxruntime as ort
from transformers import AutoModel, AutoTokenizer
import os
from fvcore.nn import FlopCountAnalysis, parameter_count_table

class TransformerToOnnx(torch.nn.Module):
    def __init__(self, model_name: str, output_dim: int):
        super().__init__()
        self.transformer = AutoModel.from_pretrained(model_name)
        self.fc = torch.nn.Linear(self.transformer.config.d_model, output_dim)

    def forward(self, input_ids: torch.Tensor, attention_mask: torch.Tensor):
        encoder_outputs = self.transformer.encoder(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state = encoder_outputs.last_hidden_state
        reduced_embedding = self.fc(last_hidden_state)
        return reduced_embedding


def prepare_sample_inputs(tokenizer, texts, max_length):
    tokens_tensor, masks_tensor = [], []
    for text in texts:
        encoded = tokenizer(
            text, padding="max_length", max_length=max_length, truncation=True, return_tensors="pt"
        )
        tokens_tensor.append(encoded["input_ids"].squeeze(0))
        masks_tensor.append(encoded["attention_mask"].squeeze(0))
    return torch.stack(tokens_tensor), torch.stack(masks_tensor)


def calculate_flops_and_parameters(model, input_ids, attention_mask):
    inputs = (input_ids, attention_mask)
    flop_analysis = FlopCountAnalysis(model, inputs)
    layer_flops = flop_analysis.by_module()
    param_table = parameter_count_table(model)
    return flop_analysis.total(), layer_flops, param_table


def main():
    model_name = "ai-forever/ruT5-base"
    output_proj_dim = 96
    max_length = 16

    model = TransformerToOnnx(model_name, output_proj_dim)
    tokenizer = AutoTokenizer.from_pretrained(model_name, legacy=True)
    model.eval()

    texts = ["Пример текста один", "Пример текста два"]
    input_ids, attention_mask = prepare_sample_inputs(tokenizer, texts, max_length)

    torch_embeddings = model(input_ids, attention_mask).detach().numpy()

    onnx_path = "models/ruT5_base_embedder.onnx"
    os.makedirs("models", exist_ok=True)
    torch.onnx.export(
        model,
        (input_ids, attention_mask),
        onnx_path,
        export_params=True,
        opset_version=17,
        input_names=["INPUT_IDS", "ATTENTION_MASK"],
        output_names=["EMBEDDINGS"],
        dynamic_axes={
            "INPUT_IDS": {0: "BATCH_SIZE"},
            "ATTENTION_MASK": {0: "BATCH_SIZE"},
            "EMBEDDINGS": {0: "BATCH_SIZE"},
        },
    )

    ort_session = ort.InferenceSession(onnx_path)
    ort_inputs = {
        "INPUT_IDS": input_ids.numpy(),
        "ATTENTION_MASK": attention_mask.numpy(),
    }
    onnx_embeddings = ort_session.run(None, ort_inputs)[0]

    assert np.allclose(torch_embeddings, onnx_embeddings, atol=1e-5), "ONNX и Torch выходы отличаются!"

    tokenizer.save_pretrained("triton/assets/tokenizer")

    total_flops, layer_flops, param_table = calculate_flops_and_parameters(model, input_ids, attention_mask)
    print(f"Суммарное количество FLOPs: {total_flops}")
    print("\nFLOPs по слоям:")
    for layer, flops in layer_flops.items():
        print(f"{layer}: {flops}")
    print("\nТаблица параметров:")
    print(param_table)

if __name__ == "__main__":
    main()
