from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="info_pandas_wbb",
    version="1.0.2",
    packages=find_packages(),
    description="Teste lib para informações de tabela pandas",
    author="William Brandão Bilatto",
    author_email="williambilatto@gmail.com",
    url='',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown"

)