"""
Configuration file for Bank Customer Churn DWH & DSS Project
Contains all paths, constants, and configuration settings
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Reports directory
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# SQL directory
SQL_DIR = PROJECT_ROOT / "sql"

# Data file paths
RAW_CHURN_FILE = RAW_DATA_DIR / "Churn_Modelling.csv"
CLEAN_CHURN_FILE = INTERIM_DATA_DIR / "churn_clean.csv"

# Processed DWH files
DIM_CUSTOMER_FILE = PROCESSED_DATA_DIR / "dim_customer.csv"
DIM_GEO_FILE = PROCESSED_DATA_DIR / "dim_geo.csv"
DIM_TIME_FILE = PROCESSED_DATA_DIR / "dim_time.csv"
DIM_SEGMENT_FILE = PROCESSED_DATA_DIR / "dim_segment.csv"
FACT_CUSTOMER_STATUS_FILE = PROCESSED_DATA_DIR / "fact_customer_status.csv"

# Data warehouse configuration
SNAPSHOT_YEAR = 2019
SNAPSHOT_MONTH = 12
SNAPSHOT_QUARTER = 4

# Feature engineering configuration
AGE_BINS = [0, 25, 35, 45, 55, 100]
AGE_LABELS = ['<=25', '26-35', '36-45', '46-55', '>=56']

INCOME_QUANTILES = 3  # Low, Mid, High
INCOME_LABELS = ['Low', 'Mid', 'High']

# Columns to drop from raw data
COLUMNS_TO_DROP = ['RowNumber', 'CustomerId', 'Surname']

# ML Model configuration
TEST_SIZE = 0.3
RANDOM_STATE = 42
STRATIFY_COLUMN = 'Exited'

# Numeric features for ML
NUMERIC_FEATURES = [
    'CreditScore',
    'Age',
    'Tenure',
    'Balance',
    'NumOfProducts',
    'EstimatedSalary'
]

# Categorical features for ML
CATEGORICAL_FEATURES = [
    'Geography',
    'Gender'
]

# Target variable
TARGET_VARIABLE = 'Exited'

# Logistic Regression parameters
LOGISTIC_MAX_ITER = 1000
LOGISTIC_RANDOM_STATE = 42

# Plotting configuration
FIGURE_DPI = 300
FIGURE_SIZE = (10, 6)
PLOT_STYLE = 'seaborn-v0_8-darkgrid'  # matplotlib style


def ensure_directories():
    """Create all necessary directories if they don't exist"""
    directories = [
        RAW_DATA_DIR,
        INTERIM_DATA_DIR,
        PROCESSED_DATA_DIR,
        FIGURES_DIR,
        SQL_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    print(f"✓ All directories created/verified under: {PROJECT_ROOT}")


if __name__ == "__main__":
    ensure_directories()
    print(f"\nProject Root: {PROJECT_ROOT}")
    print(f"Raw Data: {RAW_DATA_DIR}")
    print(f"Processed Data: {PROCESSED_DATA_DIR}")
    print(f"Figures: {FIGURES_DIR}")
