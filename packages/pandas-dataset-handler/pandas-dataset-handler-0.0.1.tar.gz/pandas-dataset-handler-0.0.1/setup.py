import os
import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

# Get version from environment variable or fallback to a default value
version = os.getenv("PACKAGE_VERSION", "0.0.1")  # Default to '0.0.1' if not provided

setuptools.setup(
    name="pandas-dataset-handler",
    version=version,  # Use the dynamic version from the environment variable
    author="Jorge Cardona",
    description="A tool to process and export datasets in various formats including ORC, Parquet, XML, JSON, HTML, CSV, HDF5, and XLSX.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jorgecardona/pandas-dataset-handler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas',
        'pyarrow',
        'pyorc',
        'lxml',
        'tables',
        'openpyxl',
    ],
)