import numpy as np

class EntropyCalculate:
    @staticmethod
    def calculate_entropy(column):
        """
        Calculate the entropy of a given column.
        :param column: pd.Series - Data column for entropy calculation.
        :return: float - Entropy value.
        """
        value_counts = column.value_counts(normalize=True)  # Get probabilities
        entropy = -np.sum(value_counts * np.log2(value_counts))  # Calculate entropy
        return entropy

    @staticmethod
    def calculate_file_entropy(df):
        """
        Calculate entropy for all columns in a DataFrame.
        :param df: pd.DataFrame
        :return: dict - Column-wise entropy values.
        """
        entropy_values = {}
        for column in df.columns:
            try:
                entropy = EntropyCalculate.calculate_entropy(df[column].dropna())
                entropy_values[column] = entropy
            except Exception as e:
                entropy_values[column] = f"Error: {e}"
        return entropy_values
