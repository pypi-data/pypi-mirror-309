# setup.py
import setuptools

from setuptools import setup, find_packages

# setup.py

from setuptools import setup, find_packages

setup(
    name="eleocm",
    version="1.0.0",
    packages=find_packages(),
    package_data={
        'eleocm': ['__pycache__/*.pyc'],  # 指定要包含的 .pyc 文件
    },
    install_requires=[
        'numpy', 'scipy',  # 依赖的库
    ],
    description="A library for calculating fuel consumption of ships.",
    author="Your Name",
    author_email="your_email@example.com",
    #url="https://github.com/yourusername/eleocm_lib",  # 如果有 GitHub 地址
)

