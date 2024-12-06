from setuptools import setup, find_packages

setup(
    name="reop",
    version="1.0.0",
    description="Rust-style Result and Option implementation for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="StatPan",
    author_email="statpan@naver.com",
    url="https://github.com/yourusername/reop",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
