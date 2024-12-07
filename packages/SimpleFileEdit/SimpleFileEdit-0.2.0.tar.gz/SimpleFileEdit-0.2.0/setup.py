from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="SimpleFileEdit",
    version="0.2.0",
    author="BravestCheetah",
    author_email="bravestcheetah@gmail.com",
    description="A tool that makes file and folder managing in python the simplest it can get!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BravestCheetah/SimpleFileEdit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Currently none but here for the future
    ],
    entry_points={
        "console_scripts": [
            # Not yet
        ],
    },
)
