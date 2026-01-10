import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import json
import matplotlib
matplotlib.use('Agg')  # Set backend for file saving
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_preprocess_data():
    """Load your fitness_data.csv and preprocess it with proper data cleaning"""
    print("Loading fitness_data.csv...")
    
    # Load your dataset
    df = pd.read_csv('fitness_data.csv')
    
    print("Dataset loaded successfully!")
    print(f"Dataset shape: {df.shape}")
    print("\nDataset columns:")
    print(df.columns.tolist())
    print("\nData types:")
    print(df.dtypes)
    print("\nFirst 5 rows:")
    print(df.head())
    
    # Map column names to standard format
    column_mapping = {}
    for col in df.columns:
        col_lower = col.lower()
        if 'weight' in col_lower:
            column_mapping[col] = 'Weight'
        elif 'height' in col_lower:
            column_mapping[col] = 'Height'
        elif 'calories' in col_lower:
            column_mapping[col] = 'Calories'
        elif 'protein' in col_lower:
            column_mapping[col] = 'Protein'
        elif 'carbs' in col_lower or 'carbohydrates' in col_lower:
            column_mapping[col] = 'Carbs'
        elif 'fat' in col_lower:
            column_mapping[col] = 'Fat'
        elif 'activity' in col_lower:
            column_mapping[col] = 'Activity_Level'
        elif 'goal' in col_lower:
            column_mapping[col] = 'Goal'
        elif 'age' in col_lower:
            column_mapping[col] = 'Age'
        elif 'gender' in col_lower:
            column_mapping[col] = 'Gender'
    
    # Rename columns to standard names
    df = df.rename(columns=column_mapping)
    
    print("\nAfter renaming columns:")
    print(df.columns.tolist())
    
    # Ensure we have all required columns
    required_columns = ['Age', 'Gender', 'Weight', 'Height', 'Activity_Level', 'Goal', 'Calories', 'Protein', 'Carbs', 'Fat']
    
    # Check for missing columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return None
    
    # Select only required columns
    df = df[required_columns]
    
    # Clean numerical columns - remove commas and convert to numeric
    numerical_columns = ['Age', 'Weight', 'Height', 'Calories', 'Protein', 'Carbs', 'Fat']
    
    for col in numerical_columns:
        if col in df.columns:
            print(f"\nCleaning column: {col}")
            print(f"Before cleaning - dtype: {df[col].dtype}")
            print(f"Sample values: {df[col].head(3).tolist()}")
            
            # Convert to string first to handle any type, then remove commas and convert to numeric
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
            
            print(f"After cleaning - dtype: {df[col].dtype}")
            print(f"Sample values: {df[col].head(3).tolist()}")
            
            # Check for NaN values after conversion
            nan_count = df[col].isna().sum()
            if nan_count > 0:
                print(f"Warning: {nan_count} NaN values in {col} after conversion")
                # Fill NaN with median
                df[col].fillna(df[col].median(), inplace=True)
    
    # Clean categorical columns
    categorical_columns = ['Gender', 'Activity_Level', 'Goal']
    for col in categorical_columns:
        if col in df.columns:
            print(f"\nCleaning categorical column: {col}")
            print(f"Unique values: {df[col].unique()}")
            # Strip whitespace and capitalize
            df[col] = df[col].astype(str).str.strip().str.title()
    
    # Remove any rows with missing values
    initial_shape = df.shape[0]
    df = df.dropna()
    final_shape = df.shape[0]
    
    if initial_shape != final_shape:
        print(f"Removed {initial_shape - final_shape} rows with missing values")
    
    print(f"\nFinal dataset shape: {df.shape}")
    print("\nFinal data types:")
    print(df.dtypes)
    print("\nFirst 3 rows of processed data:")
    print(df.head(3))
    
    # Basic statistics
    print("\nBasic statistics:")
    print(df[numerical_columns].describe())
    
    return df

def train_knn_model():
    """Train KNN model with 120 training and 80 testing instances"""
    # Load and preprocess data
    df = load_and_preprocess_data()
    
    if df is None or df.empty:
        print("Error: Dataset is empty or could not be loaded properly")
        return None, None, None, None
    
    # Ensure we have at least 200 rows
    if len(df) < 200:
        print(f"Warning: Dataset has only {len(df)} rows. Need at least 200.")
        # If we have fewer than 200, use what we have
        train_size = min(120, len(df) - 20)  # Ensure at least 20 for testing
        test_size = len(df) - train_size
    else:
        train_size = 120
        test_size = 80
    
    # Prepare features and targets
    X = df[['Age', 'Gender', 'Weight', 'Height', 'Activity_Level', 'Goal']]
    y = df[['Calories', 'Protein', 'Carbs', 'Fat']]
    
    print(f"\nFeatures shape: {X.shape}")
    print(f"Targets shape: {y.shape}")
    
    # Encode categorical variables
    label_encoders = {}
    categorical_columns = ['Gender', 'Activity_Level', 'Goal']
    
    for col in categorical_columns:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le
        print(f"Encoded {col}: {list(le.classes_)}")
    
    # Split the data: 120 training, 80 testing (or adjusted sizes)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, train_size=train_size, random_state=42
    )
    
    print(f"\n=== DATA SPLIT ===")
    print(f"Training set: {X_train.shape[0]} instances")
    print(f"Testing set: {X_test.shape[0]} instances")
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train KNN model
    print("\nTraining KNN model...")
    knn = KNeighborsRegressor(n_neighbors=5, metric='euclidean')
    knn.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_pred = knn.predict(X_test_scaled)
    
    # Calculate evaluation metrics for each target
    metrics = {}
    target_names = ['Calories', 'Protein', 'Carbs', 'Fat']
    
    for i, target in enumerate(target_names):
        metrics[target] = {
            'MAE': mean_absolute_error(y_test.iloc[:, i], y_pred[:, i]),
            'MSE': mean_squared_error(y_test.iloc[:, i], y_pred[:, i]),
            'RMSE': np.sqrt(mean_squared_error(y_test.iloc[:, i], y_pred[:, i])),
            'R2': r2_score(y_test.iloc[:, i], y_pred[:, i])
        }
    
    # Print evaluation metrics
    print(f"\n=== EVALUATION METRICS ===")
    for target in target_names:
        print(f"\n{target}:")
        for metric, value in metrics[target].items():
            print(f"  {metric}: {value:.4f}")
    
    # Create evaluation plots
    create_evaluation_plots(y_test, y_pred, target_names)
    
    # Save the model and preprocessing objects
    joblib.dump(knn, 'nutrition_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(label_encoders, 'label_encoders.pkl')
    
    # Save feature names and metrics
    with open('feature_names.json', 'w') as f:
        json.dump(list(X.columns), f)
    
    with open('evaluation_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
    
    # Save test sets for later use
    joblib.dump({'X_test': X_test, 'y_test': y_test, 'y_pred': y_pred}, 'test_sets.pkl')
    
    print("\n=== MODEL TRAINING COMPLETE ===")
    print("✅ nutrition_model.pkl - Trained KNN model")
    print("✅ scaler.pkl - Feature scaler")
    print("✅ label_encoders.pkl - Label encoders")
    print("✅ evaluation_metrics.json - Model performance metrics")
    print("✅ evaluation_plots.png - Model evaluation visualizations")
    
    return knn, scaler, label_encoders, metrics

def create_evaluation_plots(y_test, y_pred, target_names):
    """Create multiple evaluation plots"""
    plt.style.use('default')
    
    # Plot 1: Actual vs Predicted Scatter plots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('KNN Model Evaluation - Actual vs Predicted', fontsize=16, fontweight='bold')
    
    for i, target in enumerate(target_names):
        row, col = i // 2, i % 2
        axes[row, col].scatter(y_test.iloc[:, i], y_pred[:, i], alpha=0.6, color='blue')
        min_val = min(y_test.iloc[:, i].min(), y_pred[:, i].min())
        max_val = max(y_test.iloc[:, i].max(), y_pred[:, i].max())
        axes[row, col].plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
        axes[row, col].set_xlabel(f'Actual {target}')
        axes[row, col].set_ylabel(f'Predicted {target}')
        axes[row, col].set_title(f'{target}: Actual vs Predicted')
        axes[row, col].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('static/evaluation_scatter.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 2: Error Distribution
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Error Distribution for Each Target', fontsize=16, fontweight='bold')
    
    for i, target in enumerate(target_names):
        row, col = i // 2, i % 2
        errors = y_pred[:, i] - y_test.iloc[:, i]
        axes[row, col].hist(errors, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        axes[row, col].axvline(x=0, color='red', linestyle='--', linewidth=2, label='Zero Error')
        axes[row, col].axvline(x=errors.mean(), color='green', linestyle='-', linewidth=2, label=f'Mean: {errors.mean():.2f}')
        axes[row, col].set_xlabel(f'Prediction Error ({target})')
        axes[row, col].set_ylabel('Frequency')
        axes[row, col].set_title(f'{target} Error Distribution')
        axes[row, col].legend()
        axes[row, col].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('static/error_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Plot 3: Metrics Comparison Bar Chart
    metrics_data = {}
    for i, target in enumerate(target_names):
        mae = mean_absolute_error(y_test.iloc[:, i], y_pred[:, i])
        rmse = np.sqrt(mean_squared_error(y_test.iloc[:, i], y_pred[:, i]))
        metrics_data[target] = [mae, rmse]
    
    metrics_df = pd.DataFrame(metrics_data, index=['MAE', 'RMSE']).T
    
    plt.figure(figsize=(12, 6))
    ax = metrics_df.plot(kind='bar', alpha=0.8, color=['#ff9999', '#66b3ff'])
    plt.title('MAE and RMSE by Target Variable')
    plt.ylabel('Error Value')
    plt.xlabel('Target Variable')
    plt.legend(title='Metric')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # Add value labels on bars
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}', 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('static/metrics_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Evaluation plots created and saved in static/ directory")

if __name__ == "__main__":
    train_knn_model()