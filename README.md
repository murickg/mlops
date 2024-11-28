# PyTorchLightning and his friends Hydra, DVC

## 1. PyTorchLightning

Напишем простой пайплайн обучения для задачи классификации MNIST

## 2. Hydra

Для работы hydra нужно создать дирикторию ```conf``` с конфигами для модулей модели и даталоадера и добавить декоратор в модуль ```train.py``` 
```python
@hydra.main(version_base="1.3", config_path="conf", config_name="config")
def main(cfg: DictConfig)
```

Это нужно, чтобы все числовые параметры обучения задавать удобвно в одном файле, а hydra за нас все раскидает при обучении модельки

## 3. DVC

Добавим dvc для контроля версий модели, данных и экспериментов

Для начала инициализация 
```bash
dvc init
git add .dvc .gitignore
git commit -m "Initialize DVC"
```

Добавим трекинг данных
```bash
dvc add data/MNIST/raw
git add data/MNIST/raw.dvc
git commit -m "Add raw data to DVC"
```

Настроим хранилище и все запушим
```bash
dvc remote add -d storage <REMOTE_URL>
dvc push
```

Добавим dvc.yaml файл

Запустим обучение

```bash
avc repro
```

Запушим наши логи обучения

```bash
dvc add logs
git add logs.dvc
git commit -m "Add training logs"
dvc push
```
