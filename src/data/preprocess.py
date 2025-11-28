"""
Data preprocessing and feature engineering module
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import (
    COLUMNS_TO_DROP,
    AGE_BINS,
    AGE_LABELS,
    INCOME_QUANTILES,
    INCOME_LABELS,
    CLEAN_CHURN_FILE
)


def clean_data(df):
    """
    Clean the raw churn dataset
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw churn dataset
    
    Returns:
    --------
    pd.DataFrame
        Cleaned dataset
    """
    df_clean = df.copy()
    
    # Drop unnecessary columns
    print(f"Dropping columns: {COLUMNS_TO_DROP}")
    df_clean = df_clean.drop(columns=COLUMNS_TO_DROP, errors='ignore')
    
    # Check for missing values
    missing_count = df_clean.isnull().sum().sum()
    if missing_count > 0:
        print(f"Warning: Found {missing_count} missing values")
        # For this dataset, we typically don't have missing values
        # But if we did, we could handle them here
        df_clean = df_clean.dropna()
    else:
        print("✓ No missing values found")
    
    # Ensure correct data types
    df_clean['HasCrCard'] = df_clean['HasCrCard'].astype(int)
    df_clean['IsActiveMember'] = df_clean['IsActiveMember'].astype(int)
    df_clean['Exited'] = df_clean['Exited'].astype(int)
    
    print(f"✓ Data cleaned. Shape: {df_clean.shape}")
    return df_clean


def create_age_groups(df):
    """
    Create age group categories
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with 'Age' column
    
    Returns:
    --------
    pd.DataFrame
        Dataset with 'AgeGroup' column added
    """
    df = df.copy()
    df['AgeGroup'] = pd.cut(
        df['Age'],
        bins=AGE_BINS,
        labels=AGE_LABELS,
        include_lowest=True
    )
    print(f"✓ Created AgeGroup column with bins: {AGE_LABELS}")
    return df


def create_income_groups(df):
    """
    Create income group categories based on quantiles
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with 'EstimatedSalary' column
    
    Returns:
    --------
    pd.DataFrame
        Dataset with 'IncomeGroup' column added
    """
    df = df.copy()
    df['IncomeGroup'] = pd.qcut(
        df['EstimatedSalary'],
        q=INCOME_QUANTILES,
        labels=INCOME_LABELS,
        duplicates='drop'
    )
    print(f"✓ Created IncomeGroup column with labels: {INCOME_LABELS}")
    return df


def preprocess_data(df):
    """
    Complete preprocessing pipeline
    
    Parameters:
    -----------
    df : pd.DataFrame
        Raw churn dataset
    
    Returns:
    --------
    pd.DataFrame
        Fully preprocessed dataset
    """
    print("\n" + "="*60)
    print("PREPROCESSING PIPELINE")
    print("="*60 + "\n")
    
    # Step 1: Clean data
    df_processed = clean_data(df)
    
    # Step 2: Create age groups
    df_processed = create_age_groups(df_processed)
    
    # Step 3: Create income groups
    df_processed = create_income_groups(df_processed)
    
    # Step 4: Normalize Geography strings (ensure consistency)
    df_processed['Geography'] = df_processed['Geography'].str.strip()
    
    # Step 5: Normalize Gender strings
    df_processed['Gender'] = df_processed['Gender'].str.strip()
    
    print(f"\n✓ Preprocessing complete!")
    print(f"  Final shape: {df_processed.shape}")
    print(f"  New columns: AgeGroup, IncomeGroup")
    print("="*60 + "\n")
    
    return df_processed


def save_clean_data(df, file_path=None):
    """
    Save cleaned data to CSV
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned dataset
    file_path : str or Path, optional
        Output file path. If None, uses default from config.
    """
    if file_path is None:
        file_path = CLEAN_CHURN_FILE
    
    # Ensure directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(file_path, index=False)
    print(f"✓ Saved cleaned data to: {file_path}")


if __name__ == "__main__":
    from src.data.load_raw import load_raw_data
    
    # Load raw data
    df_raw = load_raw_data()
    
    # Preprocess
    df_clean = preprocess_data(df_raw)
    
    # Save
    save_clean_data(df_clean)
    
    # Show sample
    print("\nSample of cleaned data:")
    print(df_clean.head())
    print("\nColumn types:")
    print(df_clean.dtypes)
