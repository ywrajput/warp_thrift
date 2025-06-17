from setuptools import setup, find_packages

setup(
    name="warp-thrift",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "torch",
        "nvidia-ml-py3"
    ],
    author="Yousuf Rajput",
    description="A GPU stress testing and health scoring toolkit",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)