"""
Exploratory Data Analysis (EDA) plots
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import FIGURES_DIR, FIGURE_DPI, FIGURE_SIZE


def plot_churn_distribution(df, save=True, show=False):
    """
    Plot the distribution of churned vs non-churned customers
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with 'Exited' column
    save : bool
        Whether to save the figure
    show : bool
        Whether to display the figure
    """
    plt.figure(figsize=FIGURE_SIZE)
    
    churn_counts = df['Exited'].value_counts()
    labels = ['Retained (0)', 'Churned (1)']
    colors = ['#2ecc71', '#e74c3c']
    
    bars = plt.bar(labels, churn_counts.values, color=colors, alpha=0.8, edgecolor='black')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}\n({height/len(df)*100:.1f}%)',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.title('Customer Churn Distribution', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Number of Customers', fontsize=12, fontweight='bold')
    plt.xlabel('Churn Status', fontsize=12, fontweight='bold')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    if save:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES_DIR / 'churn_distribution.png'
        plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_age_distribution(df, save=True, show=False):
    """
    Plot the age distribution of customers
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with 'Age' column
    save : bool
        Whether to save the figure
    show : bool
        Whether to display the figure
    """
    plt.figure(figsize=FIGURE_SIZE)
    
    plt.hist(df['Age'], bins=30, color='#3498db', alpha=0.7, edgecolor='black')
    
    # Add mean and median lines
    mean_age = df['Age'].mean()
    median_age = df['Age'].median()
    
    plt.axvline(mean_age, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_age:.1f}')
    plt.axvline(median_age, color='green', linestyle='--', linewidth=2, label=f'Median: {median_age:.1f}')
    
    plt.title('Age Distribution of Bank Customers', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Age', fontsize=12, fontweight='bold')
    plt.ylabel('Frequency', fontsize=12, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    if save:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES_DIR / 'age_distribution.png'
        plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def plot_churn_by_geography(df, save=True, show=False):
    """
    Plot churn rate by geography
    
    Parameters:
    -----------
    df : pd.DataFrame
        Dataset with 'Geography' and 'Exited' columns
    save : bool
        Whether to save the figure
    show : bool
        Whether to display the figure
    """
    plt.figure(figsize=FIGURE_SIZE)
    
    # Calculate churn rate by geography
    churn_by_geo = df.groupby('Geography')['Exited'].agg(['sum', 'count', 'mean'])
    churn_by_geo['churn_rate'] = churn_by_geo['mean'] * 100
    churn_by_geo = churn_by_geo.sort_values('churn_rate', ascending=False)
    
    colors = ['#e74c3c', '#f39c12', '#3498db']
    bars = plt.bar(churn_by_geo.index, churn_by_geo['churn_rate'], 
                   color=colors, alpha=0.8, edgecolor='black')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        count = churn_by_geo.iloc[i]['sum']
        total = churn_by_geo.iloc[i]['count']
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%\n({int(count)}/{int(total)})',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.title('Churn Rate by Geography', fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('Churn Rate (%)', fontsize=12, fontweight='bold')
    plt.xlabel('Country', fontsize=12, fontweight='bold')
    plt.ylim(0, max(churn_by_geo['churn_rate']) * 1.2)
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    if save:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES_DIR / 'churn_by_geography.png'
        plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


def generate_all_eda_plots(df, save=True, show=False):
    """
    Generate all EDA plots at once
    
    Parameters:
    -----------
    df : pd.DataFrame
        Cleaned churn dataset
    save : bool
        Whether to save figures
    show : bool
        Whether to display figures
    """
    print("\n" + "="*60)
    print("GENERATING EDA PLOTS")
    print("="*60 + "\n")
    
    plot_churn_distribution(df, save=save, show=show)
    plot_age_distribution(df, save=save, show=show)
    plot_churn_by_geography(df, save=save, show=show)
    
    print("\n✓ All EDA plots generated!")
    print("="*60 + "\n")


if __name__ == "__main__":
    from src.config import CLEAN_CHURN_FILE
    
    # Load cleaned data
    df = pd.read_csv(CLEAN_CHURN_FILE)
    
    # Generate all plots
    generate_all_eda_plots(df, save=True, show=False)
