"""
Data Warehouse ETL module
Builds dimension and fact tables from cleaned data
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import (
    CLEAN_CHURN_FILE,
    DIM_CUSTOMER_FILE,
    DIM_GEO_FILE,
    DIM_TIME_FILE,
    DIM_SEGMENT_FILE,
    FACT_CUSTOMER_STATUS_FILE,
    SNAPSHOT_YEAR,
    SNAPSHOT_MONTH,
    SNAPSHOT_QUARTER
)


def build_dim_geo(df):
    """
    Build Geography dimension table
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned churn dataset
    
    Returns:
    --------
    pd.DataFrame
        Geography dimension with geo_key and country
    """
    # Get unique countries
    countries = df['Geography'].unique()
    
    dim_geo = pd.DataFrame({
        'geo_key': range(1, len(countries) + 1),
        'country': sorted(countries)
    })
    
    print(f"✓ Built dim_geo: {len(dim_geo)} rows")
    return dim_geo


def build_dim_time():
    """
    Build Time dimension table
    For this snapshot dataset, we create a single time record
    
    Returns:
    --------
    pd.DataFrame
        Time dimension with time_key, year, month, quarter
    """
    dim_time = pd.DataFrame({
        'time_key': [1],
        'year': [SNAPSHOT_YEAR],
        'month': [SNAPSHOT_MONTH],
        'quarter': [SNAPSHOT_QUARTER]
    })
    
    print(f"✓ Built dim_time: {len(dim_time)} rows (snapshot date)")
    return dim_time


def build_dim_segment(df):
    """
    Build Segment dimension table
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned churn dataset with AgeGroup and IncomeGroup
    
    Returns:
    --------
    pd.DataFrame
        Segment dimension with segment_key, age_group, income_group
    """
    # Get all unique combinations of age_group and income_group
    segments = df[['AgeGroup', 'IncomeGroup']].drop_duplicates().reset_index(drop=True)
    segments = segments.sort_values(['AgeGroup', 'IncomeGroup']).reset_index(drop=True)
    
    dim_segment = pd.DataFrame({
        'segment_key': range(1, len(segments) + 1),
        'age_group': segments['AgeGroup'].astype(str),
        'income_group': segments['IncomeGroup'].astype(str)
    })
    
    print(f"✓ Built dim_segment: {len(dim_segment)} rows")
    return dim_segment


def build_dim_customer(df):
    """
    Build Customer dimension table
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned churn dataset
    
    Returns:
    --------
    pd.DataFrame
        Customer dimension with customer_key and attributes
    """
    # Create customer dimension with surrogate key
    dim_customer = pd.DataFrame({
        'customer_key': range(1, len(df) + 1),
        'customer_id': df.index + 1,  # Original row index as customer ID
        'gender': df['Gender'].values,
        'age': df['Age'].values,
        'tenure': df['Tenure'].values
    })
    
    print(f"✓ Built dim_customer: {len(dim_customer)} rows")
    return dim_customer


def build_fact_customer_status(df, dim_customer, dim_geo, dim_time, dim_segment):
    """
    Build Fact table by joining cleaned data with dimension tables
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned churn dataset
    dim_customer : pd.DataFrame
        Customer dimension
    dim_geo : pd.DataFrame
        Geography dimension
    dim_time : pd.DataFrame
        Time dimension
    dim_segment : pd.DataFrame
        Segment dimension
    
    Returns:
    --------
    pd.DataFrame
        Fact table with foreign keys and measures
    """
    # Start with a copy of the cleaned data
    fact = df.copy()
    
    # Add customer_key (1:1 mapping based on row order)
    fact['customer_key'] = range(1, len(fact) + 1)
    
    # Add time_key (all records get the same snapshot time)
    fact['time_key'] = 1
    
    # Add geo_key by merging with dim_geo
    fact = fact.merge(
        dim_geo[['geo_key', 'country']],
        left_on='Geography',
        right_on='country',
        how='left'
    )
    
    # Add segment_key by merging with dim_segment
    fact['AgeGroup_str'] = fact['AgeGroup'].astype(str)
    fact['IncomeGroup_str'] = fact['IncomeGroup'].astype(str)
    
    fact = fact.merge(
        dim_segment[['segment_key', 'age_group', 'income_group']],
        left_on=['AgeGroup_str', 'IncomeGroup_str'],
        right_on=['age_group', 'income_group'],
        how='left'
    )
    
    # Select only the columns needed for the fact table
    fact_customer_status = pd.DataFrame({
        'customer_key': fact['customer_key'],
        'time_key': fact['time_key'],
        'geo_key': fact['geo_key'],
        'segment_key': fact['segment_key'],
        'balance': fact['Balance'],
        'estimated_salary': fact['EstimatedSalary'],
        'num_of_products': fact['NumOfProducts'],
        'credit_score': fact['CreditScore'],
        'has_credit_card': fact['HasCrCard'],
        'is_active_member': fact['IsActiveMember'],
        'churn_flag': fact['Exited']
    })
    
    print(f"✓ Built fact_customer_status: {len(fact_customer_status)} rows")
    return fact_customer_status


def save_dimension_and_fact_tables(dim_customer, dim_geo, dim_time, dim_segment, fact):
    """
    Save all dimension and fact tables to CSV files
    
    Parameters:
    -----------
    dim_customer : pd.DataFrame
    dim_geo : pd.DataFrame
    dim_time : pd.DataFrame
    dim_segment : pd.DataFrame
    fact : pd.DataFrame
    """
    # Ensure directory exists
    PROCESSED_DATA_DIR = DIM_CUSTOMER_FILE.parent
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save each table
    dim_customer.to_csv(DIM_CUSTOMER_FILE, index=False)
    print(f"  → Saved: {DIM_CUSTOMER_FILE.name}")
    
    dim_geo.to_csv(DIM_GEO_FILE, index=False)
    print(f"  → Saved: {DIM_GEO_FILE.name}")
    
    dim_time.to_csv(DIM_TIME_FILE, index=False)
    print(f"  → Saved: {DIM_TIME_FILE.name}")
    
    dim_segment.to_csv(DIM_SEGMENT_FILE, index=False)
    print(f"  → Saved: {DIM_SEGMENT_FILE.name}")
    
    fact.to_csv(FACT_CUSTOMER_STATUS_FILE, index=False)
    print(f"  → Saved: {FACT_CUSTOMER_STATUS_FILE.name}")
    
    print(f"\n✓ All tables saved to: {PROCESSED_DATA_DIR}")


def run_etl_pipeline(input_file=None):
    """
    Run the complete ETL pipeline to build the data warehouse
    
    Parameters:
    -----------
    input_file : str or Path, optional
        Path to cleaned data CSV. If None, uses default from config.
    """
    print("\n" + "="*60)
    print("DATA WAREHOUSE ETL PIPELINE")
    print("="*60 + "\n")
    
    # Load cleaned data
    if input_file is None:
        input_file = CLEAN_CHURN_FILE
    
    print(f"Loading cleaned data from: {input_file}")
    df = pd.read_csv(input_file)
    print(f"✓ Loaded {len(df)} records\n")
    
    # Build dimension tables
    print("Building dimension tables...")
    dim_geo = build_dim_geo(df)
    dim_time = build_dim_time()
    dim_segment = build_dim_segment(df)
    dim_customer = build_dim_customer(df)
    
    print("\nBuilding fact table...")
    fact = build_fact_customer_status(df, dim_customer, dim_geo, dim_time, dim_segment)
    
    # Save all tables
    print("\nSaving tables to CSV...")
    save_dimension_and_fact_tables(dim_customer, dim_geo, dim_time, dim_segment, fact)
    
    print("\n" + "="*60)
    print("ETL PIPELINE COMPLETE")
    print("="*60 + "\n")
    
    return dim_customer, dim_geo, dim_time, dim_segment, fact


if __name__ == "__main__":
    # Run the ETL pipeline
    dim_customer, dim_geo, dim_time, dim_segment, fact = run_etl_pipeline()
    
    # Display samples
    print("\nSample from dim_geo:")
    print(dim_geo.head())
    
    print("\nSample from dim_segment:")
    print(dim_segment.head(10))
    
    print("\nSample from fact_customer_status:")
    print(fact.head())
