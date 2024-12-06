import numpy as np
import pandas as pd

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
    def classify_entropy(entropy):
        """
        Classify entropy into pass or fail based on a threshold.
        :param entropy: float - The calculated entropy.
        :return: str - Classification of 'pass' or 'fail'.
        """
        # Set a threshold for classification (e.g., below 3 for 'pass', above for 'fail')
        threshold = 5  # Adjust this threshold value based on your needs
        if entropy < threshold:
            return 'pass'
        else:
            return 'fail'

    @staticmethod
    def calculate_file_entropy(df):
        """
        Calculate entropy for all columns in a DataFrame and classify them.
        :param df: pd.DataFrame
        :return: dict - Column-wise entropy values and classifications.
        """
        entropy_values = {}
        for column in df.columns:
            try:
                # Calculate entropy for each column
                entropy = EntropyCalculate.calculate_entropy(df[column].dropna())
                
                # Classify the column based on entropy value
                classification = EntropyCalculate.classify_entropy(entropy)
                
                # Store the entropy, classification, and column data type
                entropy_values[column] = {
                    'entropy': entropy,
                    'classification': classification,
                    'type': df[column].dtype
                }
            except Exception as e:
                entropy_values[column] = f"Error: {e}"
        return entropy_values
