"""
Churn prediction model using scikit-learn
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import (
    NUMERIC_FEATURES,
    CATEGORICAL_FEATURES,
    TARGET_VARIABLE,
    TEST_SIZE,
    RANDOM_STATE,
    LOGISTIC_MAX_ITER,
    LOGISTIC_RANDOM_STATE
)


def prepare_features_and_target(df):
    """
    Prepare features (X) and target (y) from dataset
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned churn dataset
    
    Returns:
    --------
    X : pd.DataFrame
        Feature matrix
    y : pd.Series
        Target variable
    """
    # Select features
    all_features = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    X = df[all_features].copy()
    y = df[TARGET_VARIABLE].copy()
    
    print(f"✓ Features prepared: {X.shape[1]} features, {X.shape[0]} samples")
    print(f"  Numeric features: {NUMERIC_FEATURES}")
    print(f"  Categorical features: {CATEGORICAL_FEATURES}")
    print(f"  Target variable: {TARGET_VARIABLE}")
    
    return X, y


def create_preprocessing_pipeline():
    """
    Create preprocessing pipeline with StandardScaler and OneHotEncoder
    
    Returns:
    --------
    ColumnTransformer
        Preprocessing pipeline
    """
    # Numeric transformer: StandardScaler
    numeric_transformer = StandardScaler()
    
    # Categorical transformer: OneHotEncoder
    categorical_transformer = OneHotEncoder(drop='first', sparse_output=False)
    
    # Combine transformers
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERIC_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES)
        ],
        remainder='drop'
    )
    
    return preprocessor


def build_logistic_regression_model():
    """
    Build a Logistic Regression model with preprocessing pipeline
    
    Returns:
    --------
    Pipeline
        Complete ML pipeline
    """
    preprocessor = create_preprocessing_pipeline()
    
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(
            max_iter=LOGISTIC_MAX_ITER,
            random_state=LOGISTIC_RANDOM_STATE,
            solver='lbfgs'
        ))
    ])
    
    print("✓ Created Logistic Regression pipeline")
    return model


def build_random_forest_model(n_estimators=100):
    """
    Build a Random Forest model with preprocessing pipeline
    
    Parameters:
    -----------
    n_estimators : int
        Number of trees in the forest
    
    Returns:
    --------
    Pipeline
        Complete ML pipeline
    """
    preprocessor = create_preprocessing_pipeline()
    
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=RANDOM_STATE,
            max_depth=10,
            min_samples_split=20,
            min_samples_leaf=10
        ))
    ])
    
    print(f"✓ Created Random Forest pipeline with {n_estimators} trees")
    return model


def train_model(df, model_type='logistic'):
    """
    Train a churn prediction model
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned churn dataset
    model_type : str
        Type of model: 'logistic' or 'random_forest'
    
    Returns:
    --------
    model : Pipeline
        Trained model
    X_train, X_test, y_train, y_test : arrays
        Train/test splits
    feature_names : list
        Names of features after preprocessing
    """
    print("\n" + "="*60)
    print("TRAINING CHURN PREDICTION MODEL")
    print("="*60 + "\n")
    
    # Prepare features and target
    X, y = prepare_features_and_target(df)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y
    )
    
    print(f"\n✓ Data split:")
    print(f"  Training set: {X_train.shape[0]} samples")
    print(f"  Test set: {X_test.shape[0]} samples")
    print(f"  Churn rate in train: {y_train.mean():.2%}")
    print(f"  Churn rate in test: {y_test.mean():.2%}")
    
    # Build model
    if model_type == 'logistic':
        model = build_logistic_regression_model()
    elif model_type == 'random_forest':
        model = build_random_forest_model()
    else:
        raise ValueError(f"Unknown model_type: {model_type}")
    
    # Train model
    print(f"\nTraining {model_type} model...")
    model.fit(X_train, y_train)
    print("✓ Model training complete!")
    
    # Get feature names after preprocessing
    feature_names = get_feature_names(model)
    
    print("\n" + "="*60)
    print("MODEL TRAINING COMPLETE")
    print("="*60 + "\n")
    
    return model, X_train, X_test, y_train, y_test, feature_names


def get_feature_names(model):
    """
    Extract feature names from the trained pipeline
    
    Parameters:
    -----------
    model : Pipeline
        Trained model pipeline
    
    Returns:
    --------
    list
        Feature names after preprocessing
    """
    preprocessor = model.named_steps['preprocessor']
    
    feature_names = []
    
    # Numeric features (unchanged)
    feature_names.extend(NUMERIC_FEATURES)
    
    # Categorical features (one-hot encoded)
    cat_encoder = preprocessor.named_transformers_['cat']
    cat_features = cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES)
    feature_names.extend(cat_features)
    
    return feature_names


if __name__ == "__main__":
    from src.config import CLEAN_CHURN_FILE
    
    # Load cleaned data
    df = pd.read_csv(CLEAN_CHURN_FILE)
    
    # Train model
    model, X_train, X_test, y_train, y_test, feature_names = train_model(df, model_type='logistic')
    
    # Show feature names
    print("\nFeature names after preprocessing:")
    for i, name in enumerate(feature_names, 1):
        print(f"  {i}. {name}")
