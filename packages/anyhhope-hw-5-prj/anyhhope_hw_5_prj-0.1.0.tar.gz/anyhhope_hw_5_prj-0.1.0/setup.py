from setuptools import find_packages, setup

setup(
    name="anyhhope-hw-5-prj",
    packages=find_packages(),
    data_files=[
        ("configs", ["configs/params.yaml"]),
        ("data/raw", ["data/raw/.gitkeep"]),
        ("data/processed", ["data/processed/.gitkeep"]),
    ],
    version="0.1.0",
    description="MLops project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="anyhhope",
    license="MIT",
)
