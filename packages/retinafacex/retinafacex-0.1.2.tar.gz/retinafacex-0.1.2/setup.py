from setuptools import setup, find_packages
import os

# Read the README file for the long description
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="retinafacex",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "opencv-python",
        "onnx",
        "onnxruntime",
        "requests",
        "torch"
    ],
    extras_require={
        "dev": ["pytest"],
    },
    description="RetinaFaceX (X-extended): Lightweight Face Detection Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yakhyokhuja Valikhujaev",
    author_email="yakhyo9696@gmail.com",
    url="https://github.com/yakhyo/retinafacex",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="retinaface, face detection, deep learning, onnx, opencv",
    python_requires=">=3.8",
)
