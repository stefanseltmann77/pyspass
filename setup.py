import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyspass-pkg",
    version="0.0.1",
    author="Stefan Seltmann",
    author_email="s.seltmann06@web.de",
    description="pyspass",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/stefanseltmann77/pyspass',
    packages=['pyspass'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
