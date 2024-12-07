# PandasDatasetHandler

`PandasDatasetHandler` is a Python package that provides utility functions for loading, saving, and processing datasets using Pandas DataFrames. It supports multiple file formats for reading and writing, as well as partitioning datasets into smaller chunks.

## Features
- Load datasets from multiple file formats (CSV, JSON, XML, Parquet, ORC, HDF5, etc.).
- Save datasets in various formats including CSV, JSON, Parquet, ORC, XML, HTML, HDF5, and XLSX.
- Partition a DataFrame into smaller datasets for efficient processing.
- Custom error handling for incompatible actions, formats, and processing.

## Installation

To install the package, you can use `pip`:

```bash
pip install pandas-dataset-processor
```

## Usage Example

### 1. Importing the package

```python
import pandas as pd
from pandas_dataset_handler import PandasDatasetHandler
```

### 2. Loading a dataset

You can load a dataset using the `load_dataset` method. It will automatically detect the file format based on the extension.

```python
dataset = PandasDatasetHandler.load_dataset('path/to/your/file.csv')
```

### 3. Saving a dataset

To save a DataFrame in a specific file format, use the `save_dataset` method. You can specify the directory, base filename, and the format (e.g., CSV, JSON, Parquet, etc.).

```python
PandasDatasetHandler.save_dataset(
    dataset=dataset,
    action_type='write',  # action type should be 'write' for saving
    file_format='csv',    # file format such as 'csv', 'json', 'parquet', etc.
    path='./output',      # path where the file will be saved
    base_filename='output_file'  # base filename for the saved file
)
```

### 4. Partitioning a dataset

You can partition a dataset into smaller DataFrames for distributed processing or other use cases:

```python
partitions = PandasDatasetHandler.generate_partitioned_datasets(dataset, num_parts=5)
```

### Example Code

```python
import pandas as pd
from pandas_dataset_handler import PandasDatasetHandler

dataset_1 = pd.read_csv('https://raw.githubusercontent.com/JorgeCardona/data-collection-json-csv-sql/refs/heads/main/csv/flight_logs_part_1.csv')
dataset_2 = pd.read_csv('https://raw.githubusercontent.com/JorgeCardona/data-collection-json-csv-sql/refs/heads/main/csv/flight_logs_part_2.csv')

file_formats = ['orc', 'parquet', 'xml', 'json', 'html', 'csv', 'hdf5', 'xlsx']
datasets = [dataset_1, dataset_2]
```

```python
# Example usage
file_locations = []

# Save datasets in multiple formats
for index_dataset, dataset in enumerate(datasets):
    for index_file, file_format in enumerate(file_formats):
        path = f'./data/dataset_{index_dataset+1}'
        base_filename = f'sample_dataset_{index_file+1}'
        
        file_location = f"{path}/{base_filename}.{file_format}"
        file_locations.append(file_location)
        
        PandasDatasetHandler.save_dataset(
            dataset=dataset,
            action_type='write',
            file_format=file_format,
            path=path,
            base_filename=base_filename
        )
```

```python
# Load the saved files
for file_location in file_locations:
    PandasDatasetHandler.load_dataset(file_location)
```

```python
# Generate partitioned datasets
partitions = PandasDatasetHandler.generate_partitioned_datasets(dataset_2, 7)
```

## Error Handling

The package raises custom exceptions for handling different error scenarios:
- `read_orc()` is not compatible with Windows OS.
- `IncompatibleActionError`: Raised when the specified action is not supported (e.g., trying to read a dataset when an action to write is expected).
- `IncompatibleFormatError`: Raised when the file format is not supported.
- `IncompatibleProcessingError`: Raised when neither the action nor the format is supported for processing.
- `SaveDatasetError`: Raised when an error occurs while saving a dataset in a specific format.
- `LoadDatasetError`: Raised when an error occurs while loading a file in a specific format.

## Exception Handling Example

```python
try:
    PandasDatasetHandler.save_dataset(dataset, 'write', 'xml', './output', 'example')
except SaveDatasetError as e:
    print(f"Error saving the dataset: {e}")
except IncompatibleFormatError as e:
    print(f"Unsupported format: {e}")
except IncompatibleActionError as e:
    print(f"Unsupported action: {e}")
except IncompatibleProcessingError as e:
    print(f"Processing not supported: {e}")
```

## License

This package is licensed under the MIT License. See the LICENSE file for more details.

---