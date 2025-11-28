"""
Load raw data from CSV file
"""

import pandas as pd
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import RAW_CHURN_FILE


def load_raw_data(file_path=None):
    """
    Load the raw Bank Customer Churn dataset from CSV
    
    Parameters:
    -----------
    file_path : str or Path, optional
        Path to the CSV file. If None, uses default from config.
    
    Returns:
    --------
    pd.DataFrame
        Raw churn dataset
    """
    if file_path is None:
        file_path = RAW_CHURN_FILE
    
    try:
        df = pd.read_csv(file_path)
        print(f"✓ Successfully loaded raw data from: {file_path}")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        return df
    
    except FileNotFoundError:
        print(f"✗ Error: File not found at {file_path}")
        print(f"  Please download 'Churn_Modelling.csv' from Kaggle and place it in:")
        print(f"  {RAW_CHURN_FILE.parent}")
        raise
    
    except Exception as e:
        print(f"✗ Error loading data: {str(e)}")
        raise


def get_data_summary(df):
    """
    Print a summary of the dataset
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset to summarize
    """
    print("\n" + "="*60)
    print("DATA SUMMARY")
    print("="*60)
    print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"\nColumn Types:")
    print(df.dtypes)
    print(f"\nMissing Values:")
    print(df.isnull().sum())
    print(f"\nFirst 5 rows:")
    print(df.head())
    print(f"\nBasic Statistics:")
    print(df.describe())
    print("="*60)


if __name__ == "__main__":
    # Test the loading function
    df = load_raw_data()
    get_data_summary(df)
