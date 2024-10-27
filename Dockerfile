FROM ubuntu:22.04

RUN apt update
RUN apt-get install -y g++ python3 pip tree
RUN apt-get install -y libgtest-dev
RUN apt-get install -y python3.10-venv

RUN pip install setuptools
RUN pip install pybind11
RUN pip install build
RUN pip install numpy

WORKDIR /usr/src/app
COPY ./ /usr/src/app
