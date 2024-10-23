from setuptools import setup, find_packages
from glob import glob

so_files = glob("TraceOfMatrix/python/trace_core*.so")

setup(
    name="TraceOfMatrix",
    version="0.1",
    description="Trace of matrix utility with Python bindings",
    packages=find_packages(),
    package_data={
        "TraceOfMatrix": ["python/*.so"],
    },
)