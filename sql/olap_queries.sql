-- ============================================================================
-- OLAP Queries for Bank Customer Churn Data Warehouse
-- These queries demonstrate typical analytical queries on the star schema
-- ============================================================================

-- Query 1: Overall Churn Rate
-- Calculate the overall churn rate across all customers
SELECT 
    COUNT(*) AS total_customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100, 2) AS churn_rate_pct
FROM fact_customer_status;


-- Query 2: Churn Rate by Country
-- Analyze churn rate across different countries
SELECT 
    g.country,
    COUNT(*) AS total_customers,
    SUM(f.churn_flag) AS churned_customers,
    ROUND(AVG(f.churn_flag) * 100, 2) AS churn_rate_pct
FROM fact_customer_status f
JOIN dim_geo g ON f.geo_key = g.geo_key
GROUP BY g.country
ORDER BY churn_rate_pct DESC;


-- Query 3: Churn Rate by Age Group
-- Analyze churn rate across different age segments
SELECT 
    s.age_group,
    COUNT(*) AS total_customers,
    SUM(f.churn_flag) AS churned_customers,
    ROUND(AVG(f.churn_flag) * 100, 2) AS churn_rate_pct
FROM fact_customer_status f
JOIN dim_segment s ON f.segment_key = s.segment_key
GROUP BY s.age_group
ORDER BY 
    CASE s.age_group
        WHEN '<=25' THEN 1
        WHEN '26-35' THEN 2
        WHEN '36-45' THEN 3
        WHEN '46-55' THEN 4
        WHEN '>=56' THEN 5
    END;


-- Query 4: Churn Rate by Income Group
-- Analyze churn rate across different income segments
SELECT 
    s.income_group,
    COUNT(*) AS total_customers,
    SUM(f.churn_flag) AS churned_customers,
    ROUND(AVG(f.churn_flag) * 100, 2) AS churn_rate_pct
FROM fact_customer_status f
JOIN dim_segment s ON f.segment_key = s.segment_key
GROUP BY s.income_group
ORDER BY 
    CASE s.income_group
        WHEN 'Low' THEN 1
        WHEN 'Mid' THEN 2
        WHEN 'High' THEN 3
    END;


-- Query 5: Average Balance by Churn Status
-- Compare average account balance between churned and retained customers
SELECT 
    CASE 
        WHEN churn_flag = 0 THEN 'Retained'
        WHEN churn_flag = 1 THEN 'Churned'
    END AS customer_status,
    COUNT(*) AS customer_count,
    ROUND(AVG(balance), 2) AS avg_balance,
    ROUND(AVG(estimated_salary), 2) AS avg_salary,
    ROUND(AVG(credit_score), 2) AS avg_credit_score
FROM fact_customer_status
GROUP BY churn_flag
ORDER BY churn_flag;


-- Query 6: Churn Rate by Number of Products
-- Analyze how product ownership affects churn
SELECT 
    num_of_products,
    COUNT(*) AS total_customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100, 2) AS churn_rate_pct
FROM fact_customer_status
GROUP BY num_of_products
ORDER BY num_of_products;


-- Query 7: Churn Rate by Active Membership Status
-- Compare churn between active and inactive members
SELECT 
    CASE 
        WHEN is_active_member = 0 THEN 'Inactive'
        WHEN is_active_member = 1 THEN 'Active'
    END AS membership_status,
    COUNT(*) AS total_customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100, 2) AS churn_rate_pct
FROM fact_customer_status
GROUP BY is_active_member
ORDER BY is_active_member DESC;


-- Query 8: Top 10 Segments with Highest Churn Rate
-- Identify customer segments most at risk
SELECT 
    s.age_group,
    s.income_group,
    g.country,
    COUNT(*) AS total_customers,
    SUM(f.churn_flag) AS churned_customers,
    ROUND(AVG(f.churn_flag) * 100, 2) AS churn_rate_pct
FROM fact_customer_status f
JOIN dim_segment s ON f.segment_key = s.segment_key
JOIN dim_geo g ON f.geo_key = g.geo_key
GROUP BY s.age_group, s.income_group, g.country
HAVING COUNT(*) >= 10  -- Only segments with at least 10 customers
ORDER BY churn_rate_pct DESC
LIMIT 10;


-- Query 9: Customer Profile Comparison (Churned vs Retained)
-- Detailed comparison of customer characteristics
SELECT 
    CASE 
        WHEN churn_flag = 0 THEN 'Retained'
        WHEN churn_flag = 1 THEN 'Churned'
    END AS customer_status,
    COUNT(*) AS customer_count,
    ROUND(AVG(c.age), 1) AS avg_age,
    ROUND(AVG(c.tenure), 1) AS avg_tenure,
    ROUND(AVG(f.balance), 2) AS avg_balance,
    ROUND(AVG(f.estimated_salary), 2) AS avg_salary,
    ROUND(AVG(f.credit_score), 1) AS avg_credit_score,
    ROUND(AVG(f.num_of_products), 2) AS avg_num_products,
    ROUND(AVG(f.has_credit_card) * 100, 1) AS pct_with_credit_card,
    ROUND(AVG(f.is_active_member) * 100, 1) AS pct_active_members
FROM fact_customer_status f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY churn_flag
ORDER BY churn_flag;


-- Query 10: Churn Rate by Gender and Country
-- Cross-dimensional analysis
SELECT 
    g.country,
    c.gender,
    COUNT(*) AS total_customers,
    SUM(f.churn_flag) AS churned_customers,
    ROUND(AVG(f.churn_flag) * 100, 2) AS churn_rate_pct
FROM fact_customer_status f
JOIN dim_customer c ON f.customer_key = c.customer_key
JOIN dim_geo g ON f.geo_key = g.geo_key
GROUP BY g.country, c.gender
ORDER BY g.country, c.gender;


-- Query 11: High-Value Customer Churn Analysis
-- Focus on customers with high balance
SELECT 
    CASE 
        WHEN balance >= 100000 THEN 'High Balance (>=100K)'
        WHEN balance >= 50000 THEN 'Medium Balance (50K-100K)'
        ELSE 'Low Balance (<50K)'
    END AS balance_category,
    COUNT(*) AS total_customers,
    SUM(churn_flag) AS churned_customers,
    ROUND(AVG(churn_flag) * 100, 2) AS churn_rate_pct,
    ROUND(AVG(balance), 2) AS avg_balance
FROM fact_customer_status
GROUP BY 
    CASE 
        WHEN balance >= 100000 THEN 'High Balance (>=100K)'
        WHEN balance >= 50000 THEN 'Medium Balance (50K-100K)'
        ELSE 'Low Balance (<50K)'
    END
ORDER BY avg_balance DESC;


-- Query 12: Tenure Analysis
-- How customer tenure affects churn
SELECT 
    c.tenure,
    COUNT(*) AS total_customers,
    SUM(f.churn_flag) AS churned_customers,
    ROUND(AVG(f.churn_flag) * 100, 2) AS churn_rate_pct
FROM fact_customer_status f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.tenure
ORDER BY c.tenure;

-- ============================================================================
-- END OF OLAP QUERIES
-- ============================================================================
