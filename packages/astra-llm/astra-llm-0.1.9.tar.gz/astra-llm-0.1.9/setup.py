from setuptools import setup, find_packages

# Read the requirements from requirements.txt
with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name="astra-llm",
    version="0.1.9",
    author="Md. Golam Mostofa",
    author_email="golammostofa10001@gmail.com",
    description="Astra is a lightweight library for Astra LLM.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/shuvo881/Astra",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11.0',
    install_requires=install_requires,
)