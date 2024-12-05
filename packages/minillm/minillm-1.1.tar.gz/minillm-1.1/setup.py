import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="minillm",
    version="1.1",
    author="AKM Korishee Apurbo",
    author_email="bandinvisible8@gmail.com",
    description="Simple inference for large language models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IMApurbo/minillm",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "huggingface_hub",
        "ctranslate2>=4.4.0",
        "tokenizers",
       ],
)
