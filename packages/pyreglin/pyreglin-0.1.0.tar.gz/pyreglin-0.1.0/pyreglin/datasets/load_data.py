import requests
import os
import sys
from pathlib import Path

import pandas as pd


def get_data_home(data_home=None):
    """
    Return a path to the cache directory for datasets.

    This directory is used for storing datasets that need to be loaded
    in the future. If the directory does not exist, it will be created.

    Parameters:
    ----------
    data_home : str, optional
        The directory where datasets are cached. If None, it will default
        to a user-specific cache directory.

    Returns
    -------
    data_home : str
        The path to the cache directory.
    """
    if data_home is None:
        # Default to the directory where the pyreglin package is installed
        package_path = Path(sys.modules['pyreglin'].__file__).parent
        data_home = os.path.join(package_path, 'data')

    # Ensure the directory exists
    if not os.path.exists(data_home):
        os.makedirs(data_home)
    
    return data_home


def load_data(name, cache=True, data_home=None, **kwargs):
    """
    Load a dataset, either from cache or by downloading it from the internet.
    
    Parameters:
    ----------
    name : str
        The name of the dataset (assumes the dataset is available online as a CSV).
    cache : bool, optional
        If True, it will check if the dataset is cached locally and load from there.
        If False, it will always download the dataset.
    data_home : str, optional
        The directory where datasets are cached. If None, it defaults to a user cache directory.
    kwargs : additional arguments
        Arguments passed to `pandas.read_csv` when reading the dataset.

    Returns
    -------
    df : pandas.DataFrame
        The loaded dataset as a DataFrame.
    """
    # Base URL for datasets
    dataset_url = f"https://raw.githubusercontent.com/salvnetto/pyreglin/refs/heads/main/datasets/{name}.csv"
    
    # Get the cache directory
    cache_dir = get_data_home(data_home)
    cached_file_path = os.path.join(cache_dir, f"{name}.csv")

    # Load from cache or download
    if cache and os.path.exists(cached_file_path):
        print(cached_file_path)
        df = pd.read_csv(cached_file_path, **kwargs)
    else:
        response = requests.get(dataset_url)
        
        if response.status_code == 200:
            # Save the dataset to the cache directory
            print(cached_file_path)
            with open(cached_file_path, 'wb') as f:
                f.write(response.content)
            # Load the dataset into a DataFrame
            df = pd.read_csv(cached_file_path, **kwargs)
        else:
            raise ValueError(f"Failed to download {name}. HTTP Status: {response.status_code}")
    
    return df




df = load_data("tensao", cache=True)

# Display the first few rows
print(df.head())