# TensorRT, Triton

## Проделанная работа

Экспорт модели в ONNX, работа с Nvidia Triton Inference Server, компиляция в TensorRT

Итак, для начала запустим скрипт ```torch2onnx.py``` для конвертации модели в ONNX.

Далее хотим сконвертировать модель в tenosRT. Для этого запустим соответсвующий контенйнер (```Dockerfile1```) и запустим скрипт ```convert_to_tensorrt.sh```

После того, как получим соответствующие ```.plan``` файлы, нужно их положить в model_repository.

Также в model_repository добавляем наш токенизатор. 

После чего запустим tritonserver

Как видим, он работает
![работа triton](pic1.png)

Так же напишем клиента ```client.py``` и чекнем, как различаются наши модели с onnx
![клиентский сервис](pic2.png)

Отчет о FLOPs в файле flops.txt

Также нам интересно затестить наш сервер. Сделаем это при помощи
```bash
docker run --rm --network="host" nvcr.io/nvidia/tritonserver:23.04-py3-sdk perf_analyzer -m <model_name> -u <server_url> --concurrency-range 1:32 > <report_name>.txt
```
Подробные отчеты от ```perf_analyzer``` представленны в директории ```perf_analyzer```.
  