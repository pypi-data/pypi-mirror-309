from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="plantigo-common",
    version="1.0.8",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.70.0",
        "grpcio>=1.39.0",
        "grpc-interceptor>=0.15.4",
        "python-jose>=3.3.0",
        "djangorestframework>=3.15.2",
        "protobuf>=5.28.3",
    ],
    description="Reusable modules for Plantigo project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="jakubaniszewski@pm.me",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
