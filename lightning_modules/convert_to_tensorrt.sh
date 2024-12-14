#!/bin/bash

ONNX_MODEL_PATH="models/model.onnx"

OUTPUT_DIR="triton/model_repository"
mkdir -p $OUTPUT_DIR


PRECISION_FLAGS=("--fp16" "--int8" "--best" "")
PRECISION_NAMES=("FP16" "INT8" "BEST" "FP32")

MIN_SHAPES="INPUT_IDS:1x16,ATTENTION_MASK:1x16"
OPT_SHAPES="INPUT_IDS:4x16,ATTENTION_MASK:4x16"
MAX_SHAPES="INPUT_IDS:8x16,ATTENTION_MASK:8x16"

for i in "${!PRECISION_FLAGS[@]}"; do
    PRECISION="${PRECISION_FLAGS[$i]}"
    OUTPUT_FILE="${OUTPUT_DIR}/model_TRT_${PRECISION_NAMES[$i]}.plan"

    echo "Конвертация модели с точностью ${PRECISION_NAMES[$i]}..."

    trtexec \
        --onnx=$ONNX_MODEL_PATH \
        --saveEngine=$OUTPUT_FILE \
        --minShapes=$MIN_SHAPES \
        --optShapes=$OPT_SHAPES \
        --maxShapes=$MAX_SHAPES \
        $PRECISION

    if [ $? -eq 0 ]; then
        echo "Модель успешно сохранена: $OUTPUT_FILE"
    else
        echo "Ошибка при конвертации модели с точностью ${PRECISION_NAMES[$i]}."
        exit 1
    fi
done

echo "Все модели TensorRT успешно конвертированы!"
