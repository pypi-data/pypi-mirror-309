from io import open
from setuptools import setup, find_packages

"""
:authors: fofmow
:license: MIT
"""

version = "2.0.1"

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()


if __name__ == "__main__":
    setup(
        name="aiomoney",
        version=version,

        author="fofmow",
        author_email="fofmow@gmail.com",

        description="Простая асинхронная библиотека для работы с API ЮMoney",
        long_description=long_description,
        long_description_content_type="text/markdown",
        
        url="https://github.com/fofmow/aiomoney",
        download_url="https://github.com/fofmow/aiomoney",
        license="MIT",
        packages=find_packages(),
        install_requires=["aiohttp>=3.9.5", "pydantic>=2.8"],
        classifiers=[
            "Programming Language :: Python :: 3.10",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
        ],
        keywords="yoomoney python async",
        python_requires=">=3.10"
    )
