-- ============================================================================
-- Data Warehouse Schema DDL for Bank Customer Churn Analysis
-- Database: PostgreSQL
-- Schema: Star Schema with Fact and Dimension Tables
-- ============================================================================

-- Drop existing tables if they exist (for clean recreation)
DROP TABLE IF EXISTS fact_customer_status CASCADE;
DROP TABLE IF EXISTS dim_customer CASCADE;
DROP TABLE IF EXISTS dim_geo CASCADE;
DROP TABLE IF EXISTS dim_time CASCADE;
DROP TABLE IF EXISTS dim_segment CASCADE;

-- ============================================================================
-- DIMENSION TABLES
-- ============================================================================

-- Geography Dimension
CREATE TABLE dim_geo (
    geo_key SERIAL PRIMARY KEY,
    country VARCHAR(50) NOT NULL UNIQUE
);

COMMENT ON TABLE dim_geo IS 'Geography dimension containing country information';
COMMENT ON COLUMN dim_geo.geo_key IS 'Surrogate key for geography';
COMMENT ON COLUMN dim_geo.country IS 'Country name';

-- Time Dimension
CREATE TABLE dim_time (
    time_key SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4)
);

COMMENT ON TABLE dim_time IS 'Time dimension for snapshot dates';
COMMENT ON COLUMN dim_time.time_key IS 'Surrogate key for time';
COMMENT ON COLUMN dim_time.year IS 'Year of snapshot';
COMMENT ON COLUMN dim_time.month IS 'Month of snapshot';
COMMENT ON COLUMN dim_time.quarter IS 'Quarter of snapshot (1-4)';

-- Segment Dimension
CREATE TABLE dim_segment (
    segment_key SERIAL PRIMARY KEY,
    age_group VARCHAR(20) NOT NULL,
    income_group VARCHAR(20) NOT NULL,
    UNIQUE(age_group, income_group)
);

COMMENT ON TABLE dim_segment IS 'Customer segment dimension based on age and income groups';
COMMENT ON COLUMN dim_segment.segment_key IS 'Surrogate key for segment';
COMMENT ON COLUMN dim_segment.age_group IS 'Age group category (<=25, 26-35, 36-45, 46-55, >=56)';
COMMENT ON COLUMN dim_segment.income_group IS 'Income group category (Low, Mid, High)';

-- Customer Dimension
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL UNIQUE,
    gender VARCHAR(10) NOT NULL,
    age INTEGER NOT NULL CHECK (age >= 18 AND age <= 100),
    tenure INTEGER NOT NULL CHECK (tenure >= 0 AND tenure <= 10)
);

COMMENT ON TABLE dim_customer IS 'Customer dimension with demographic attributes';
COMMENT ON COLUMN dim_customer.customer_key IS 'Surrogate key for customer';
COMMENT ON COLUMN dim_customer.customer_id IS 'Original customer identifier';
COMMENT ON COLUMN dim_customer.gender IS 'Customer gender (Male/Female)';
COMMENT ON COLUMN dim_customer.age IS 'Customer age in years';
COMMENT ON COLUMN dim_customer.tenure IS 'Years as bank customer (0-10)';

-- ============================================================================
-- FACT TABLE
-- ============================================================================

-- Customer Status Fact Table
CREATE TABLE fact_customer_status (
    customer_key INTEGER NOT NULL,
    time_key INTEGER NOT NULL,
    geo_key INTEGER NOT NULL,
    segment_key INTEGER NOT NULL,
    balance DECIMAL(12, 2) NOT NULL DEFAULT 0,
    estimated_salary DECIMAL(12, 2) NOT NULL,
    num_of_products INTEGER NOT NULL CHECK (num_of_products BETWEEN 1 AND 4),
    credit_score INTEGER NOT NULL CHECK (credit_score BETWEEN 300 AND 850),
    has_credit_card INTEGER NOT NULL CHECK (has_credit_card IN (0, 1)),
    is_active_member INTEGER NOT NULL CHECK (is_active_member IN (0, 1)),
    churn_flag INTEGER NOT NULL CHECK (churn_flag IN (0, 1)),
    
    -- Foreign key constraints
    CONSTRAINT fk_customer FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    CONSTRAINT fk_time FOREIGN KEY (time_key) REFERENCES dim_time(time_key),
    CONSTRAINT fk_geo FOREIGN KEY (geo_key) REFERENCES dim_geo(geo_key),
    CONSTRAINT fk_segment FOREIGN KEY (segment_key) REFERENCES dim_segment(segment_key),
    
    -- Composite primary key
    PRIMARY KEY (customer_key, time_key)
);

COMMENT ON TABLE fact_customer_status IS 'Fact table containing customer status metrics and churn information';
COMMENT ON COLUMN fact_customer_status.customer_key IS 'Foreign key to dim_customer';
COMMENT ON COLUMN fact_customer_status.time_key IS 'Foreign key to dim_time';
COMMENT ON COLUMN fact_customer_status.geo_key IS 'Foreign key to dim_geo';
COMMENT ON COLUMN fact_customer_status.segment_key IS 'Foreign key to dim_segment';
COMMENT ON COLUMN fact_customer_status.balance IS 'Account balance in dollars';
COMMENT ON COLUMN fact_customer_status.estimated_salary IS 'Estimated annual salary in dollars';
COMMENT ON COLUMN fact_customer_status.num_of_products IS 'Number of bank products (1-4)';
COMMENT ON COLUMN fact_customer_status.credit_score IS 'Credit score (300-850)';
COMMENT ON COLUMN fact_customer_status.has_credit_card IS 'Has credit card flag (0=No, 1=Yes)';
COMMENT ON COLUMN fact_customer_status.is_active_member IS 'Active member flag (0=No, 1=Yes)';
COMMENT ON COLUMN fact_customer_status.churn_flag IS 'Churn flag (0=Retained, 1=Churned)';

-- ============================================================================
-- INDEXES for Performance
-- ============================================================================

-- Indexes on foreign keys
CREATE INDEX idx_fact_customer ON fact_customer_status(customer_key);
CREATE INDEX idx_fact_time ON fact_customer_status(time_key);
CREATE INDEX idx_fact_geo ON fact_customer_status(geo_key);
CREATE INDEX idx_fact_segment ON fact_customer_status(segment_key);

-- Index on churn_flag for filtering
CREATE INDEX idx_fact_churn ON fact_customer_status(churn_flag);

-- Composite indexes for common queries
CREATE INDEX idx_fact_geo_churn ON fact_customer_status(geo_key, churn_flag);
CREATE INDEX idx_fact_segment_churn ON fact_customer_status(segment_key, churn_flag);

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
