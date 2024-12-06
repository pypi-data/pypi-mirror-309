from setuptools import setup, find_packages

setup(
    name="trembala",
    version="0.0.0",
    author="Artur Arantes Santos da Silva",
    author_email="contact@trembao.dev",
    description="Trembala: Um framework inovador e rápido.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ArturArantes/trembala",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
