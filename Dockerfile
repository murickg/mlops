# Используем базовый образ с Python
FROM python:3.11-slim

RUN apt update
RUN apt-get install tree

WORKDIR /usr/src/app

COPY ./ /usr/src/app

RUN pip install build wheel numpy

RUN python3 -m build

RUN pip3 install dist/TraceOfMatrix-*.whl

