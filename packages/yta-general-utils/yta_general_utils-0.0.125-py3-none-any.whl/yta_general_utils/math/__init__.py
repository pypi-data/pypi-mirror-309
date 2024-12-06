import numpy as np


class Math:
    """
    Class to simplify and encapsulate functionality related
    to math that could be more complex than the contained 
    in the basic python math module.
    """
    @staticmethod
    def sigmoid(value):
        """
        TODO: Write doc about this
        """
        return 1.0 / (1 + np.exp(-value))
    
    @staticmethod
    def normalize(value, min_value, max_value):
        """
        Normalize the provided 'value' to turn it into another
        value between 0.0 and 1.0.
        """
        return (value - min_value) / (max_value - min_value)

    @staticmethod
    def denormalize(value, min_value, max_value):
        """
        Denormalize the provided 'value' (that must be between
        0.0 and 1.0) by turning it into another value between
        the provided 'min_value' and 'max_value'.
        """
        return value * (max_value - min_value) + min_value