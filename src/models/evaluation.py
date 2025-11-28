"""
Model evaluation functions
"""

import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve
)
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import FIGURES_DIR, FIGURE_DPI


def evaluate_model(model, X_test, y_test, verbose=True):
    """
    Evaluate model performance
    
    Parameters:
    -----------
    model : sklearn model
        Trained model
    X_test : pd.DataFrame
        Test features
    y_test : pd.Series
        Test target
    verbose : bool
        Whether to print results
    
    Returns:
    --------
    dict
        Dictionary with evaluation metrics
    """
    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)
    class_report = classification_report(y_test, y_pred, target_names=['Retained', 'Churned'])
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    
    if verbose:
        print("\n" + "="*60)
        print("MODEL EVALUATION RESULTS")
        print("="*60 + "\n")
        
        print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"ROC-AUC Score: {roc_auc:.4f}\n")
        
        print("Confusion Matrix:")
        print(conf_matrix)
        print()
        
        print("Classification Report:")
        print(class_report)
        
        print("="*60 + "\n")
    
    return {
        'accuracy': accuracy,
        'confusion_matrix': conf_matrix,
        'classification_report': class_report,
        'roc_auc': roc_auc,
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba
    }


def plot_confusion_matrix(conf_matrix, save=True, show=False):
    """
    Plot confusion matrix
    
    Parameters:
    -----------
    conf_matrix : array
        Confusion matrix
    save : bool
        Whether to save the figure
    show : bool
        Whether to display the figure
    """
    plt.figure(figsize=(8, 6))
    
    plt.imshow(conf_matrix, interpolation='nearest', cmap='Blues')
    plt.title('Confusion Matrix', fontsize=16, fontweight='bold', pad=20)
    plt.colorbar()
    
    classes = ['Retained', 'Churned']
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, fontsize=12)
    plt.yticks(tick_marks, classes, fontsize=12)
    
    # Add text annotations
    thresh = conf_matrix.max() / 2.
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            plt.text(j, i, format(conf_matrix[i, j], 'd'),
                    ha="center", va="center",
                    color="white" if conf_matrix[i, j] > thresh else "black",
                    fontsize=14, fontweight='bold')
    
    plt.ylabel('True Label', fontsize=12, fontweight='bold')
    plt.xlabel('Predicted Label', fontsize=12, fontweight='bold')
    plt.tight_layout()
    
    if save:
        FIGURES_DIR.mkdir(parents=True, exist_ok=True)
        output_path = FIGURES_DIR / 'confusion_matrix.png'
        plt.savefig(output_path, dpi=FIGURE_DPI, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    if show:
        plt.show()
    else:
        plt.close()


if __name__ == "__main__":
    from src.config import CLEAN_CHURN_FILE
    from src.models.churn_model import train_model
    
    # Load data and train model
    df = pd.read_csv(CLEAN_CHURN_FILE)
    model, X_train, X_test, y_train, y_test, feature_names = train_model(df)
    
    # Evaluate
    results = evaluate_model(model, X_test, y_test)
    
    # Plot confusion matrix
    plot_confusion_matrix(results['confusion_matrix'], save=True, show=False)
