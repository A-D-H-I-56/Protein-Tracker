import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Load .env
load_dotenv(dotenv_path=BASE_DIR / '.env', override=False)

import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error
from app.config import Config

def generate_evaluation_visualizations(artifacts_dir: str = None, output_dirs: list = None):
    """
    Generates high-res visual performance plots from persisted test evaluations.
    """
    artifacts_dir = artifacts_dir or Config.ARTIFACTS_DIR
    artifacts_path = Path(artifacts_dir)
    test_sets_path = artifacts_path / 'test_sets.pkl'

    if not test_sets_path.exists():
        print(f"Test sets not found at {test_sets_path}. Run training pipeline first.")
        return

    data = joblib.load(test_sets_path)
    y_test = data['y_test']
    y_pred = data['y_pred']
    target_names = data['target_names']

    if output_dirs is None:
        output_dirs = [Path(Config.STATIC_FOLDER) / "images"]

    for out_dir in output_dirs:
        out_dir.mkdir(parents=True, exist_ok=True)

    plt.style.use('default')

    # 1. Actual vs Predicted Scatter Plots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('KNN AI Model Performance - Ground Truth vs Predicted', fontsize=16, fontweight='bold', color='#1e293b')

    colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']

    for i, target in enumerate(target_names):
        row, col = i // 2, i % 2
        ax = axes[row, col]
        y_true_col = y_test.iloc[:, i]
        y_pred_col = y_pred[:, i]

        ax.scatter(y_true_col, y_pred_col, alpha=0.7, color=colors[i], edgecolors='w', s=50)
        min_v = min(y_true_col.min(), y_pred_col.min())
        max_v = max(y_true_col.max(), y_pred_col.max())
        ax.plot([min_v, max_v], [min_v, max_v], 'r--', lw=2, label='Perfect Fit')

        ax.set_title(f'{target} Targets', fontweight='600')
        ax.set_xlabel(f'Actual {target}')
        ax.set_ylabel(f'Predicted {target}')
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend()

    plt.tight_layout()
    for out_dir in output_dirs:
        plt.savefig(out_dir / 'evaluation_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Residual / Error Distribution Plots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Prediction Residual Distribution across Targets', fontsize=16, fontweight='bold', color='#1e293b')

    for i, target in enumerate(target_names):
        row, col = i // 2, i % 2
        ax = axes[row, col]
        errors = y_pred[:, i] - y_test.iloc[:, i]

        ax.hist(errors, bins=18, alpha=0.75, color=colors[i], edgecolor='black')
        ax.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Zero Error')
        ax.axvline(x=errors.mean(), color='navy', linestyle='-', linewidth=2, label=f'Mean Error: {errors.mean():.2f}')

        ax.set_title(f'{target} Residuals', fontweight='600')
        ax.set_xlabel(f'Residual (Predicted - Actual)')
        ax.set_ylabel('Frequency')
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend()

    plt.tight_layout()
    for out_dir in output_dirs:
        plt.savefig(out_dir / 'error_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. MAE & RMSE Metrics Comparison Bar Chart
    metrics_data = {}
    for i, target in enumerate(target_names):
        mae = mean_absolute_error(y_test.iloc[:, i], y_pred[:, i])
        rmse = np.sqrt(mean_squared_error(y_test.iloc[:, i], y_pred[:, i]))
        metrics_data[target] = [mae, rmse]

    metrics_df = pd.DataFrame(metrics_data, index=['MAE', 'RMSE']).T

    fig, ax = plt.subplots(figsize=(10, 6))
    metrics_df.plot(kind='bar', ax=ax, color=['#6366f1', '#06b6d4'], alpha=0.85, edgecolor='none')
    ax.set_title('Error Metrics by Target (MAE vs RMSE)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Error Value')
    ax.set_xlabel('Target Variable')
    ax.grid(True, linestyle=':', alpha=0.6)
    plt.xticks(rotation=0)

    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{height:.1f}', (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=9, fontweight='bold', xytext=(0, 2),
                        textcoords='offset points')

    plt.tight_layout()
    for out_dir in output_dirs:
        plt.savefig(out_dir / 'metrics_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("Model evaluation diagnostic plots generated successfully!")

if __name__ == "__main__":
    generate_evaluation_visualizations()
