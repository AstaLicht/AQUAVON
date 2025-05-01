
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Load dataset (Replace with actual dataset)
df = pd.read_csv("water_quality_data.csv")

# Handle missing values
df.fillna(df.mean(), inplace=True)

# Define Features (Inputs) and Targets (Outputs)
X = df[['Temperature', 'pH', 'TDS', 'Turbidity']]
y_do = df['DO']
y_metal = df['Heavy_Metal_Concentration']
y_bacteria = df['Bacterial_Contamination']

# Train-test split
X_train, X_test, y_do_train, y_do_test = train_test_split(X, y_do, test_size=0.2, random_state=42)
X_train, X_test, y_metal_train, y_metal_test = train_test_split(X, y_metal, test_size=0.2, random_state=42)
X_train, X_test, y_bacteria_train, y_bacteria_test = train_test_split(X, y_bacteria, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Models
do_model = RandomForestRegressor(n_estimators=100, random_state=42)
do_model.fit(X_train_scaled, y_do_train)

metal_model = RandomForestRegressor(n_estimators=100, random_state=42)
metal_model.fit(X_train_scaled, y_metal_train)

bacteria_model = RandomForestClassifier(n_estimators=100, random_state=42)
bacteria_model.fit(X_train_scaled, y_bacteria_train)

# Save Models
joblib.dump(do_model, "do_model.pkl")
joblib.dump(metal_model, "metal_model.pkl")
joblib.dump(bacteria_model, "bacteria_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Models & Scaler Saved Successfully!")
