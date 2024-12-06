"""
Provides config for model initialization
"""

from pydantic import BaseModel

class DataConfig(BaseModel):
    """
    Class to configure dataset
    Parameters:
        n_samples: number of samples to generate
        n_features: number of features
        n_classes: number of classes
        random_state: random_state
        test_size: part of generated data wich will be left for test
    """
    n_samples: int = 1000
    n_features: int = 20
    n_classes: int = 2
    random_state: int = 42
    test_size: float = 0.2
