# Quick Start Guide - Bank Customer Churn DWH & DSS

## 🚀 Quick Start (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download Dataset
- Go to Kaggle: [Bank Customer Churn Modeling](https://www.kaggle.com/datasets/shantanudhakadd/bank-customer-churn-prediction)
- Download `Churn_Modelling.csv`
- Place it in: `data/raw/Churn_Modelling.csv`

### 3. Run the Pipeline
```bash
# Preprocess data and build data warehouse
python src/data/preprocess.py
python src/data/dwh_etl.py
```

### 4. Launch Dashboard
```bash
python run_dashboard.py
```

Open browser to: **http://localhost:8050**

---

## 📊 Dashboard Overview

The interactive dashboard provides:

### KPI Cards (Top Row)
- **Total Customers**: Count of all customers in dataset
- **Churned**: Number of customers who left
- **Churn Rate**: Percentage of customers who churned
- **Avg Balance**: Average account balance across all customers

### Interactive Filters
- **Country**: Filter by France, Germany, or Spain
- **Age Group**: Filter by age ranges (<=25, 26-35, 36-45, 46-55, >=56)
- **Gender**: Filter by Male or Female

### Visualizations
1. **Churn Rate by Country**: Bar chart showing which countries have highest churn
2. **Churn Rate by Age Group**: Bar chart showing age-based churn patterns
3. **Balance Distribution**: Box plot comparing account balances of churned vs retained
4. **Churn by Products**: Bar chart showing how product count affects churn
5. **Age Distribution**: Histogram of customer ages
6. **Churn by Tenure**: Line chart showing churn trends over customer tenure

---

## 🎯 Use Cases

### For Business Analysts
- Identify high-risk customer segments
- Compare churn rates across countries
- Analyze impact of product ownership on retention

### For Data Scientists
- Explore feature distributions
- Validate preprocessing results
- Identify patterns for model features

### For Executives
- Monitor key churn metrics
- Get quick insights with KPI cards
- Make data-driven retention decisions

---

## 💡 Tips

1. **Start with "All" filters** to see overall patterns
2. **Drill down** by selecting specific countries or age groups
3. **Compare segments** by switching between filter combinations
4. **Look for patterns** in the interactive charts
5. **Export insights** by taking screenshots for reports

---

## 🔧 Troubleshooting

### Dashboard won't start
```bash
# Make sure dependencies are installed
pip install dash plotly

# Check if data is preprocessed
python src/data/preprocess.py
```

### No data showing
- Ensure `data/interim/churn_clean.csv` exists
- Run preprocessing: `python src/data/preprocess.py`

### Port already in use
Edit `src/visualization/dashboard.py` and change port:
```python
dashboard.run(debug=True, port=8051)  # Change to different port
```

---

## 📚 Next Steps

After exploring the dashboard:
1. Run Jupyter notebooks for detailed analysis
2. Train ML model: `python src/models/churn_model.py`
3. Generate static plots: `python src/visualization/eda_plots.py`
4. Explore SQL queries in `sql/olap_queries.sql`

Enjoy exploring the data! 🎉
