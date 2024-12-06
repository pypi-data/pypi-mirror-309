from setuptools import setup, find_packages

setup(
    name="ATEM",
    version="1.0.1",
    packages=find_packages(include=["atem_core", "atem_core.*", "auto", "auto.*"]),
    install_requires=[
        "tensorflow",
        "numpy",
    ],
)
