import pandas as pd

class FileImport:
    @staticmethod
    def file_import(file_path):
        """
        Load an Excel file into a pandas DataFrame.
        :param file_path: str - Path to the Excel file.
        :return: pd.DataFrame
        """
        try:
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            raise ValueError(f"Error loading file: {e}")
