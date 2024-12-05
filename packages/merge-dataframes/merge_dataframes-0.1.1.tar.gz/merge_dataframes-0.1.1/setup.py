from setuptools import setup, find_packages

setup(
    name="merge_dataframes",
    version="0.1.1",
    description="A Python package to merge two Pandas DataFrames",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Laxman Kusuma",
    author_email="laxman.kusuma@gmail.com",
    url="https://github.com/laxmankusuma/merge_dataframes",
    packages=find_packages(),  # Automatically discovers all packages
    install_requires=[
        "pandas>=1.0.0"
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
