# Bank Customer Churn Data Warehouse & Decision Support System

A complete Python-based data warehouse and decision support system for analyzing bank customer churn, built for university coursework in "Data Warehouse & Decision Support System".

## 📊 Project Overview

This project implements a full end-to-end data warehouse solution for bank customer churn analysis, including:

- **Star Schema Data Warehouse** with dimension and fact tables
- **ETL Pipeline** for data extraction, transformation, and loading
- **Machine Learning Model** for churn prediction
- **Python-based Visualizations** for exploratory analysis and reporting
- **SQL Queries** for OLAP-style analytics

## 🗂️ Project Structure

```
bank_churn_dwh_dss/
├── data/
│   ├── raw/                    # Raw dataset (Churn_Modelling.csv)
│   ├── interim/                # Cleaned, preprocessed data
│   └── processed/              # Dimension and fact tables (CSV)
├── sql/
│   ├── create_dwh_schema.sql   # DDL for star schema
│   └── olap_queries.sql        # Sample OLAP queries
├── src/
│   ├── config.py               # Configuration and paths
│   ├── data/
│   │   ├── load_raw.py         # Load raw CSV
│   │   ├── preprocess.py       # Data cleaning & feature engineering
│   │   └── dwh_etl.py          # Build dimension/fact tables
│   ├── visualization/
│   │   ├── eda_plots.py        # Exploratory data analysis plots
│   │   └── churn_dashboard_plots.py  # Dashboard-style plots
│   └── models/
│       ├── churn_model.py      # ML model training
│       └── evaluation.py       # Model evaluation
├── notebooks/
│   ├── 01_eda_and_cleaning.ipynb
│   ├── 02_build_dwh_and_olap.ipynb
│   └── 03_churn_modeling_and_viz.ipynb
├── reports/
│   └── figures/                # Generated PNG plots
└── README.md
```

## 📦 Dataset

**Source**: Kaggle - Bank Customer Churn Modeling  
**File**: `Churn_Modelling.csv`  
**Size**: 10,000 rows × 14 columns

### Columns:
- `RowNumber`, `CustomerId`, `Surname` (dropped during preprocessing)
- `CreditScore`, `Geography`, `Gender`, `Age`, `Tenure`
- `Balance`, `NumOfProducts`, `HasCrCard`, `IsActiveMember`
- `EstimatedSalary`, `Exited` (target variable: 0=Retained, 1=Churned)

**⚠️ Important**: Download the dataset from Kaggle and place it at:  
`data/raw/Churn_Modelling.csv`

## 🏗️ Data Warehouse Design

### Star Schema

**Fact Table**: `fact_customer_status`
- Grain: One row per customer snapshot
- Measures: `balance`, `estimated_salary`, `num_of_products`, `credit_score`
- Flags: `has_credit_card`, `is_active_member`, `churn_flag`
- Foreign Keys: `customer_key`, `time_key`, `geo_key`, `segment_key`

**Dimension Tables**:
- `dim_customer`: Customer demographics (age, gender, tenure)
- `dim_geo`: Geography (country)
- `dim_time`: Snapshot time (year, month, quarter)
- `dim_segment`: Customer segments (age group, income group)

## 🚀 Getting Started

### Prerequisites

```bash
# Python 3.11+ required
python --version

# Install required packages
pip install pandas numpy matplotlib scikit-learn

# For interactive dashboard (optional)
pip install dash plotly
```

### Setup

1. **Clone/Download** this project
2. **Download dataset** from Kaggle and place at `data/raw/Churn_Modelling.csv`
3. **Create directories**:
   ```bash
   cd bank_churn_dwh_dss
   python src/config.py
   ```

### Running the Pipeline

#### Option 1: Run Python Modules Directly

```bash
# Step 1: Load and preprocess data
python src/data/load_raw.py
python src/data/preprocess.py

# Step 2: Build data warehouse
python src/data/dwh_etl.py

# Step 3: Generate visualizations
python src/visualization/eda_plots.py
python src/visualization/churn_dashboard_plots.py

# Step 4: Train and evaluate model
python src/models/churn_model.py
python src/models/evaluation.py
```

#### Option 2: Use Jupyter Notebooks

```bash
jupyter notebook
```

Then run notebooks in order:
1. `01_eda_and_cleaning.ipynb` - Data exploration and preprocessing
2. `02_build_dwh_and_olap.ipynb` - Build DWH and run OLAP queries
3. `03_churn_modeling_and_viz.ipynb` - Train ML model and generate visualizations

#### Option 3: Interactive Dashboard (Recommended!)

```bash
# Launch the interactive web dashboard
python run_dashboard.py
```

Then open your browser to: **http://localhost:8050**

**Dashboard Features:**
- 📊 Real-time KPI cards (Total Customers, Churned, Churn Rate, Avg Balance)
- 🔍 Interactive filters (Country, Age Group, Gender)
- 📈 6 interactive charts:
  - Churn Rate by Country
  - Churn Rate by Age Group
  - Balance Distribution by Churn Status
  - Churn Rate by Number of Products
  - Customer Age Distribution
  - Churn Rate by Tenure
- 🎨 Modern, responsive UI with Plotly visualizations

## 📈 Outputs

### Generated Files

**Data Files** (in `data/processed/`):
- `dim_customer.csv`
- `dim_geo.csv`
- `dim_time.csv`
- `dim_segment.csv`
- `fact_customer_status.csv`

**Visualizations** (in `reports/figures/`):
- `churn_distribution.png` - Overall churn distribution
- `age_distribution.png` - Age distribution histogram
- `churn_by_geography.png` - Churn rate by country
- `balance_by_churn.png` - Average balance comparison
- `churn_by_age_group.png` - Churn rate by age group
- `churn_by_products.png` - Churn rate by number of products
- `feature_importance.png` - ML model feature importance
- `confusion_matrix.png` - Model evaluation confusion matrix

## 🤖 Machine Learning

### Model: Logistic Regression (Baseline)

**Features**:
- Numeric: `CreditScore`, `Age`, `Tenure`, `Balance`, `NumOfProducts`, `EstimatedSalary`
- Categorical: `Geography`, `Gender`

**Preprocessing**:
- StandardScaler for numeric features
- OneHotEncoder for categorical features

**Evaluation Metrics**:
- Accuracy
- Confusion Matrix
- Classification Report (Precision, Recall, F1-Score)
- ROC-AUC Score

### Optional: Random Forest

Change model type in `churn_model.py`:
```python
model, X_train, X_test, y_train, y_test, feature_names = train_model(df, model_type='random_forest')
```

## 📊 SQL Queries

The `sql/olap_queries.sql` file contains 12 analytical queries, including:
- Overall churn rate
- Churn rate by country, age group, income group
- Average balance by churn status
- Customer profile comparison
- High-value customer analysis
- And more...

To use these queries, load the CSV files into a PostgreSQL database using the schema in `sql/create_dwh_schema.sql`.

## 🎓 Educational Value

This project demonstrates:
- ✅ Data warehouse dimensional modeling (star schema)
- ✅ ETL pipeline design and implementation
- ✅ Data preprocessing and feature engineering
- ✅ OLAP-style analytical queries
- ✅ Machine learning for predictive analytics
- ✅ Data visualization for decision support
- ✅ Clean code organization and modularity

## 📝 License

This project is for educational purposes as part of university coursework.

## 👤 Author



## 🙏 Acknowledgments

- Dataset: Kaggle Bank Customer Churn Modeling
- Course: Data Warehouse & Decision Support System
