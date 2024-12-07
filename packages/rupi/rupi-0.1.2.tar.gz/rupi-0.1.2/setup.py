from setuptools import setup, find_packages

setup(
    name="rupi",
    version="0.1.2",
    description="A Python library for my codes.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TanujairamV/pali",
    author="Tanujairam",
    author_email="tanujairam.v@gmail.com",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
