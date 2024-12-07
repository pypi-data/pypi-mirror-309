import logging
import os
import pandas as pd

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

class IncompatibleActionError(Exception):
    """Exception raised when the action is not supported."""
    def __init__(self, action_type: str):
        super().__init__(f"Action '{action_type}' is not supported.")

class IncompatibleFormatError(Exception):
    """Exception raised when the file format is not supported."""
    def __init__(self, file_format: str):
        super().__init__(f"Format '{file_format}' is not supported.")

class IncompatibleProcessingError(Exception):
    """Exception raised when the processing is not supported."""
    def __init__(self):
        super().__init__("Processing is not supported. The file was neither saved nor processed.")

class SaveDatasetError(Exception):
    """
    Custom exception for errors when saving a DataFrame in a specific format.
    """
    def __init__(self, file_format, original_exception):
        super().__init__(f"Error saving the file in format '{file_format}': {original_exception}")
        self.file_format = file_format
        self.original_exception = original_exception

class LoadDatasetError(Exception):
    """
    Custom exception for errors when loading a file in a specific format.
    """
    def __init__(self, file_path, file_format, original_exception):
        super().__init__(f"Error loading the file '{file_path}' with format '{file_format}': {original_exception}")
        self.file_path = file_path
        self.file_format = file_format
        self.original_exception = original_exception

class PandasDatasetHandler:

    @staticmethod
    def create_directory_if_not_exists(path: str) -> None:
        """
        Checks if the specified directory exists. If not, creates it.

        Args:
            path (str): Directory path to check.

        Returns:
            None
        """
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Directorio '{path}' creado.")

    @staticmethod
    def compatible_formats(action_type: str, file_format: str, dataset: pd.DataFrame = None):
        """
        Returns compatible methods for reading or writing data based on the action type and format.
    
        Parameters:
        - action_type (str): The action type, either 'write' or 'read'.
        - file_format (str): The file format, such as 'csv', 'json', 'xml', etc.
        - dataset (pd.DataFrame, optional): The DataFrame to process (required for write actions).
    
        Returns:
        - dict: A dictionary with compatible actions for the specified action type.
        - callable or None: A callable function for the specified format or None if not supported.
        """
        compatible_formats = {
            'write': {
                'orc': lambda filename: dataset.to_orc(filename) if dataset is not None else None,
                'parquet': lambda filename: dataset.to_parquet(filename) if dataset is not None else None,
                'xml': lambda filename: dataset.to_xml(filename, index=False) if dataset is not None else None,
                'json': lambda filename: dataset.to_json(filename, orient='records', lines=False, indent=4) if dataset is not None else None,
                'html': lambda filename: dataset.to_html(filename, index=False, border=1) if dataset is not None else None,
                'hdf5': lambda filename: dataset.to_hdf(filename, key='df', mode='w') if dataset is not None else None,
                'csv': lambda filename: dataset.to_csv(filename, encoding='utf-8', index=False) if dataset is not None else None,
                'xlsx': lambda filename: dataset.to_excel(filename, engine='openpyxl', index=False) if dataset is not None else None
            },
            'read': {
                'orc': pd.read_orc,
                'parquet': pd.read_parquet,
                'xml': pd.read_xml,
                'json': pd.read_json,
                'html': pd.read_html,
                'csv': pd.read_csv,
                'hdf5': pd.read_hdf,
                'xlsx': pd.read_excel
            }
        }
    
        compatible_action_type = compatible_formats.get(action_type, {})
        compatible_file_format = compatible_action_type.get(file_format.lower(), None)
    
        return compatible_action_type, compatible_file_format

    @staticmethod
    def save_dataset(dataset: pd.DataFrame, action_type: str, file_format: str, path: str = '.', base_filename: str = 'output_file') -> None:
        """
        Saves a DataFrame in the specified file format.
    
        Parameters:
        - dataset (pd.DataFrame): The DataFrame to save.
        - action_type (str): The type of action ('write' to save).
        - file_format (str): The file format, such as 'csv', 'json', 'xml', etc.
        - path (str): The directory path where the file will be saved (default is the current directory).
        - base_filename (str): The base name for the file (default is 'output_file').
    
        Raises:
        - SaveDatasetError: If an error occurs while saving the file.
        - IncompatibleProcessingError: If neither the action nor the format is supported.
        - IncompatibleActionError: If the action type is not supported.
        - IncompatibleFormatError: If the file format is not supported.
        """
        compatible_action_type, compatible_file_format = PandasDatasetHandler.compatible_formats(action_type, file_format, dataset)
    
        if compatible_action_type and compatible_file_format:
            PandasDatasetHandler.create_directory_if_not_exists(path)
            file_name = os.path.join(path, f'{base_filename}.{file_format.lower()}')
    
            try:
                compatible_file_format(file_name) # Save the file in the specified format
                print(f"File Saved as {file_name}")
            except Exception as e:
                raise SaveDatasetError(file_format, e)
        else:
            if not compatible_action_type and not compatible_file_format:
                raise IncompatibleProcessingError()
            elif not compatible_action_type:
                raise IncompatibleActionError(action_type)
            elif not compatible_file_format:
                raise IncompatibleFormatError(file_format)

    @staticmethod
    def load_dataset(file_path: str) -> pd.DataFrame:
        """
        Loads a dataset from a file, automatically determining the format based on the file extension.
    
        Args:
            file_path (str): The full path of the file to load.
    
        Returns:
            pd.DataFrame: The loaded dataset as a DataFrame.
    
        Raises:
            LoadDatasetError: If an error occurs while attempting to load the file.
            IncompatibleFormatError: If the file format is not compatible.
        """
        file_format = file_path.split('.')[-1]  # Get the file extension
        compatible_action_type, compatible_file_format = PandasDatasetHandler.compatible_formats('read', file_format)
    
        if compatible_file_format:
            try:
                # Read the file using the corresponding method
                dataset = compatible_file_format(file_path)
                print(f"File '{file_path}' successfully loaded as {file_format}.")
                return dataset
            except Exception as e:
                # Raise a custom exception if an error occurs during loading
                raise LoadDatasetError(file_path, file_format, e)
        else:
            # Raise a custom exception if the format is not compatible
            raise IncompatibleFormatError(file_format)
  
    @staticmethod
    def generate_partitioned_datasets(dataset: pd.DataFrame, num_parts: int) -> list:
        """
        Divides a DataFrame into 'n' partitions evenly. If an exact division is not possible, 
        the last partition will contain the remaining records, with the remainder distributed as 
        evenly as possible among the earlier partitions.
    
        Parameters:
        dataset (pd.DataFrame): The DataFrame to be divided.
        num_parts (int): The number of partitions to divide the DataFrame into.
    
        Returns:
        list: A list of DataFrames generated from the partitioning of the original DataFrame.
        """
    
        # dataset total records
        total_rows = len(dataset)
        
        # Calculate the base size of the partitions and the remaining records
        base_partition_size = total_rows // num_parts
        remainder = total_rows % num_parts
        
        partitions = []
        start_idx = 0
        
        # Create the partitions, distributing the remaining records evenly
        for i in range(num_parts):
            # The partition size will be base_partition_size + 1 for the first 'remainder' partitions
            partition_size = base_partition_size + (1 if i < remainder else 0)
            end_idx = start_idx + partition_size
            partitions.append(dataset.iloc[start_idx:end_idx])
            start_idx = end_idx
        
        return partitions