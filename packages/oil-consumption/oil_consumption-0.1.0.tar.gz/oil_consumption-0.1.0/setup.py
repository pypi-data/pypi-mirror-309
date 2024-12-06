# setup.py
import setuptools

from setuptools import setup, find_packages

setup(
    name="oil_consumption", #模块名称
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
    ],
    description="A library to calculate oil consumption based on ship speed, wind speed, and sea wave height.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Zesheng Jing",
    author_email="394050399@qq.com",
    #url="https://github.com/yourusername/oil_consumption",  # Replace with your actual URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
