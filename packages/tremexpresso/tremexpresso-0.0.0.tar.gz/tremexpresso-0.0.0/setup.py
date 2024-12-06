from setuptools import setup, find_packages

setup(
    name="tremexpresso",
    version="0.0.0",
    author="Artur Arantes Santos da Silva",
    author_email="contact@trembao.dev",
    description="TremExpresso: Rapidez e eficiência em um framework inovador.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ArturArantes/tremexpresso",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
