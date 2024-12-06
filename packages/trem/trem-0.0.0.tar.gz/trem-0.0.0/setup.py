from setuptools import setup, find_packages

setup(
    name="trem",
    version="0.0.0",
    author="Artur Arantes Santos da Silva",
    author_email="contact@trembao.dev",
    description="Trem: Um framework inovador.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ArturArantes/trem",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
