from setuptools import setup, find_packages

setup(
    name="plantigo-common",
    version="1.0.6",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.70.0",
        "grpcio>=1.39.0",
        "grpc-interceptor>=0.15.4",
        "python-jose>=3.3.0",
    ],
    description="Reusable modules for Plantigo project",
    author="jakubaniszewski@pm.me",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
