# TraceOfMatrix
Питоновский биндинг для расчета следа матрицы. 

Создаем docker image 
```bash
docker build -t trace .
```

Запускаем контейнер в интерактивном режиме
```bash
docker run --rm -it trace /bin/bash
```

Собираем объектные файлы, устанавливаем наш пакет.
```bash
make TraceOfMatrix
python3 -m build
pip3 install dist/*.whl
```

Запускаем скрипт, который сравнивает время работы биндинга с реализацией numpy
```bash
python3 perf.py
```

Радуемся :)
