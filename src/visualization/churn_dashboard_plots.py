"""
Dashboard-style plots for churn analysis and reporting
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import FIGURES_DIR, FIGURE_DPI, FIGURE_SIZE


def plot_balance_by_churn(df, save=True, show=False):
    """
    Plot average balance for churned vs non-churned customers
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with 'Balance' and 'Exited' columns
    save : bool
        Whether to save the figure
    show : bool
        Whether to display the figure
    """
    plt.figure(figsize=FIGURE_SIZE)
    
    # Calculate average balance by churn status
    balance_by_churn = df.groupby('Exited')['Balance'].mean()
    labels = ['Retained (0)', 'Churned (1)']
    colors = ['#2ecc71', '#e74c3c']
    
    bars = plt.bar(labels, balance_by_churn.values, color=colors, alpha=0.8, edgecolor='black')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.title('Average Account Balance by Churn Status', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Average Balance ($)', fontsize=12, fontweight='bold')
    plt.xlabel('Churn Status', fontsize=12, fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    if save:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES_DIR / 'balance_by_churn.png'
        plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_churn_by_age_group(df, save=True, show=False):
    """
    Plot churn rate by age group
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with 'AgeGroup' and 'Exited' columns
    save : bool
        Whether to save the figure
    show : bool
        Whether to display the figure
    """
    plt.figure(figsize=FIGURE_SIZE)
    
    # Calculate churn rate by age group
    churn_by_age = df.groupby('AgeGroup')['Exited'].agg(['sum', 'count', 'mean'])
    churn_by_age['churn_rate'] = churn_by_age['mean'] * 100
    
    # Ensure proper ordering of age groups
    age_order = ['<=25', '26-35', '36-45', '46-55', '>=56']
    churn_by_age = churn_by_age.reindex(age_order)
    
    colors = ['#3498db', '#2ecc71', '#f39c12', '#e67e22', '#e74c3c']
    bars = plt.bar(churn_by_age.index, churn_by_age['churn_rate'], 
                   color=colors, alpha=0.8, edgecolor='black')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        count = churn_by_age.iloc[i]['sum']
        total = churn_by_age.iloc[i]['count']
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%\n({int(count)}/{int(total)})',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.title('Churn Rate by Age Group', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Churn Rate (%)', fontsize=12, fontweight='bold')
    plt.xlabel('Age Group', fontsize=12, fontweight='bold')
    plt.ylim(0, max(churn_by_age['churn_rate']) * 1.25)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    if save:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES_DIR / 'churn_by_age_group.png'
        plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_feature_importance(model, feature_names, save=True, show=False, top_n=10):
    """
    Plot feature importance from a trained model
    For LogisticRegression: plots absolute coefficient values
    For tree-based models: plots feature_importances_
    
    Parameters:
    -----------
    model : sklearn model
        Trained model (should be the final estimator from pipeline)
    feature_names : list
        List of feature names after preprocessing
    save : bool
        Whether to save the figure
    show : bool
        Whether to display the figure
    top_n : int
        Number of top features to display
    """
    plt.figure(figsize=(10, 8))
    
    # Get feature importance based on model type
    if hasattr(model, 'coef_'):
        # Logistic Regression or linear models
        importance = np.abs(model.coef_[0])
        title = 'Feature Importance (Absolute Coefficient Values)'
    elif hasattr(model, 'feature_importances_'):
        # Tree-based models
        importance = model.feature_importances_
        title = 'Feature Importance (Tree-based)'
    else:
        print("Warning: Model does not have coefficients or feature importances")
        return
    
    # Create DataFrame for easier sorting
    feature_importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importance
    }).sort_values('importance', ascending=True).tail(top_n)
    
    # Plot horizontal bar chart
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(feature_importance_df)))
    bars = plt.barh(feature_importance_df['feature'], feature_importance_df['importance'],
                    color=colors, alpha=0.8, edgecolor='black')
    
    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Importance', fontsize=12, fontweight='bold')
    plt.ylabel('Feature', fontsize=12, fontweight='bold')
    plt.grid(axis='x', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    if save:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES_DIR / 'feature_importance.png'
        plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_churn_by_products(df, save=True, show=False):
    """
    Plot churn rate by number of products
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with 'NumOfProducts' and 'Exited' columns
    save : bool
        Whether to save the figure
    show : bool
        Whether to display the figure
    """
    plt.figure(figsize=FIGURE_SIZE)
    
    # Calculate churn rate by number of products
    churn_by_products = df.groupby('NumOfProducts')['Exited'].agg(['sum', 'count', 'mean'])
    churn_by_products['churn_rate'] = churn_by_products['mean'] * 100
    
    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']
    bars = plt.bar(churn_by_products.index.astype(str), churn_by_products['churn_rate'],
                   color=colors[:len(churn_by_products)], alpha=0.8, edgecolor='black')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        count = churn_by_products.iloc[i]['sum']
        total = churn_by_products.iloc[i]['count']
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%\n({int(count)}/{int(total)})',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.title('Churn Rate by Number of Products', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Churn Rate (%)', fontsize=12, fontweight='bold')
    plt.xlabel('Number of Products', fontsize=12, fontweight='bold')
    plt.ylim(0, max(churn_by_products['churn_rate']) * 1.25)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    if save:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES_DIR / 'churn_by_products.png'
        plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def generate_all_dashboard_plots(df, model=None, feature_names=None, save=True, show=False):
    """
    Generate all dashboard plots at once
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned churn dataset
    model : sklearn model, optional
        Trained model for feature importance plot
    feature_names : list, optional
        Feature names for importance plot
    save : bool
        Whether to save figures
    show : bool
        Whether to display figures
    """
    print("\n" + "="*60)
    print("GENERATING DASHBOARD PLOTS")
    print("="*60 + "\n")
    
    plot_balance_by_churn(df, save=save, show=show)
    plot_churn_by_age_group(df, save=save, show=show)
    plot_churn_by_products(df, save=save, show=show)
    
    if model is not None and feature_names is not None:
        plot_feature_importance(model, feature_names, save=save, show=show)
    
    print("\n✓ All dashboard plots generated!")
    print("="*60 + "\n")


if __name__ == "__main__":
    from src.config import CLEAN_CHURN_FILE
    
    # Load cleaned data
    df = pd.read_csv(CLEAN_CHURN_FILE)
    
    # Generate all plots (without model-based plots)
    generate_all_dashboard_plots(df, save=True, show=False)
