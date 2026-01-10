from flask import Flask, render_template, request, jsonify
import joblib
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Global variables for model and preprocessing objects
model = None
scaler = None
label_encoders = None
feature_names = None
evaluation_metrics = None

def load_model():
    """Load the trained model and preprocessing objects"""
    global model, scaler, label_encoders, feature_names, evaluation_metrics
    try:
        model = joblib.load('nutrition_model.pkl')
        scaler = joblib.load('scaler.pkl')
        label_encoders = joblib.load('label_encoders.pkl')
        
        with open('feature_names.json', 'r') as f:
            feature_names = json.load(f)
            
        with open('evaluation_metrics.json', 'r') as f:
            evaluation_metrics = json.load(f)
            
        print("✅ Model and preprocessing objects loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

# Load model when app starts
load_model()

@app.route('/')
def index():
    """Render the main form page"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle form submission and display results"""
    if model is None:
        return render_template('result.html', 
                             error='Model not loaded properly. Please check if model files exist.')
    
    try:
        # Get form data
        age = int(request.form['age'])
        gender = request.form['gender']
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        activity_level = request.form['activity_level']
        goal = request.form['goal']
        
        # Validate inputs
        if age < 15 or age > 100:
            return render_template('result.html', error='Age must be between 15 and 100')
        if weight < 40 or weight > 200:
            return render_template('result.html', error='Weight must be between 40 and 200 kg')
        if height < 140 or height > 220:
            return render_template('result.html', error='Height must be between 140 and 220 cm')
        
        # Prepare input features
        input_data = pd.DataFrame([{
            'Age': age,
            'Gender': gender,
            'Weight': weight,
            'Height': height,
            'Activity_Level': activity_level,
            'Goal': goal
        }])
        
        # Encode categorical variables
        for col in ['Gender', 'Activity_Level', 'Goal']:
            if col in label_encoders:
                le = label_encoders[col]
                if input_data[col].iloc[0] in le.classes_:
                    input_data[col] = le.transform([input_data[col].iloc[0]])[0]
                else:
                    return render_template('result.html', error=f'Invalid value for {col}')
        
        # Ensure correct column order
        input_data = input_data[feature_names]
        
        # Scale the features
        input_scaled = scaler.transform(input_data)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        
        # Extract values
        calories = int(round(prediction[0]))
        protein = int(round(prediction[1]))
        carbs = int(round(prediction[2]))
        fat = int(round(prediction[3]))
        
        # Validate prediction results
        if calories < 1000 or calories > 5000:
            return render_template('result.html', error='Prediction out of reasonable range. Please check your inputs.')
        
        # Calculate macro ratios
        protein_ratio = round((protein * 4) / calories * 100) if calories > 0 else 0
        carbs_ratio = round((carbs * 4) / calories * 100) if calories > 0 else 0
        fat_ratio = round((fat * 9) / calories * 100) if calories > 0 else 0
        
        # Create a simple performance plot for this prediction
        plot_url = create_single_prediction_plot(calories, protein, carbs, fat)
        
        # Prepare result data
        result_data = {
            'age': age,
            'gender': gender,
            'weight': weight,
            'height': height,
            'activity_level': activity_level,
            'goal': goal,
            'calories': calories,
            'protein': protein,
            'carbs': carbs,
            'fat': fat,
            'protein_ratio': protein_ratio,
            'carbs_ratio': carbs_ratio,
            'fat_ratio': fat_ratio,
            'plot_url': plot_url,
            'metrics': evaluation_metrics
        }
        
        return render_template('result.html', **result_data)
        
    except Exception as e:
        return render_template('result.html', error=f'Prediction error: {str(e)}')

def create_single_prediction_plot(calories, protein, carbs, fat):
    """Create a visualization for the single prediction"""
    plt.figure(figsize=(10, 8))
    
    # Create subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Plot 1: Macronutrient distribution (Pie chart)
    macros = [protein, carbs, fat]
    macro_labels = [f'Protein\n{protein}g', f'Carbs\n{carbs}g', f'Fat\n{fat}g']
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    ax1.pie(macros, labels=macro_labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Macronutrient Distribution')
    
    # Plot 2: Calorie breakdown (Bar chart)
    nutrient_names = ['Protein', 'Carbs', 'Fat']
    calorie_breakdown = [protein * 4, carbs * 4, fat * 9]
    bars = ax2.bar(nutrient_names, calorie_breakdown, color=colors, alpha=0.8)
    ax2.set_ylabel('Calories')
    ax2.set_title('Calorie Contribution by Macronutrient')
    
    # Add value labels on bars
    for bar, value in zip(bars, calorie_breakdown):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, 
                f'{value} kcal', ha='center', va='bottom')
    
    # Plot 3: Macronutrient ratios (Bar chart)
    ratios = [
        round((protein * 4) / calories * 100),
        round((carbs * 4) / calories * 100),
        round((fat * 9) / calories * 100)
    ]
    bars = ax3.bar(nutrient_names, ratios, color=colors, alpha=0.8)
    ax3.set_ylabel('Percentage (%)')
    ax3.set_title('Macronutrient Ratio (%)')
    ax3.set_ylim(0, 100)
    
    # Add value labels on bars
    for bar, value in zip(bars, ratios):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                f'{value}%', ha='center', va='bottom')
    
    # Plot 4: Total calories
    ax4.bar(['Total Calories'], [calories], color='#ffcc99', alpha=0.8)
    ax4.set_ylabel('Calories')
    ax4.set_title(f'Daily Calorie Target: {calories:,} kcal')
    ax4.text(0, calories + 50, f'{calories:,} kcal', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    # Save plot to bytes
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=150, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return f"data:image/png;base64,{plot_url}"

@app.route('/metrics')
def show_metrics():
    """Display evaluation metrics page"""
    if evaluation_metrics is None:
        return "Evaluation metrics not available"
    
    return render_template('metrics.html', metrics=evaluation_metrics)

if __name__ == '__main__':
    print("🚀 Starting Fitness Nutrition Calculator Flask App...")
    print("📊 Model trained on 200 instances (120 train, 80 test)")
    print("📈 Evaluation metrics and plots available")
    print("🌐 Web interface available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)