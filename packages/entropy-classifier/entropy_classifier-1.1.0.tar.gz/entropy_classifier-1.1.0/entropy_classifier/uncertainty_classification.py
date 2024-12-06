class UncertaintyClassification:
    @staticmethod
    def classify_columns_by_uncertainty(entropy_values):
        """
        Classify columns based on certainty levels.
        :param entropy_values: dict - Column-wise entropy values.
        :return: dict - Classification results for each column.
        """
        classification_results = {}
        for column, entropy in entropy_values.items():
            if isinstance(entropy, float):  # Ensure entropy is a number
                certainty_to_fail = (1 - 2 ** (-entropy)) * 100
                certainty_to_pass = 100 - certainty_to_fail
                classification = "pass" if certainty_to_pass > certainty_to_fail else "fail"
                classification_results[column] = {
                    "entropy": entropy,
                    "certainty_to_pass": certainty_to_pass,
                    "certainty_to_fail": certainty_to_fail,
                    "classification": classification,
                }
            else:
                classification_results[column] = {"error": entropy}
        return classification_results
