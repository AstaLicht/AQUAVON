import joblib
import numpy as np

# Load trained models
do_model = joblib.load("do_model.pkl")
metal_model = joblib.load("metal_model.pkl")
bacteria_model = joblib.load("bacteria_model.pkl")
scaler = joblib.load("scaler.pkl")

# Example real-time input
real_time_data = np.array([[5.5, 1.5, 754.0, 500.0]])  # Temp, pH, TDS, Turbidity

# Scale input data
real_time_scaled = scaler.transform(real_time_data)

# Predict DO, Heavy Metals, and Bacteria
pred_do = do_model.predict(real_time_scaled)[0]
pred_metal = metal_model.predict(real_time_scaled)[0]
pred_bacteria = bacteria_model.predict(real_time_scaled)[0]

# Output Results
print(f"Dissolved Oxygen (DO): {pred_do:.2f} mg/L")
print(f"Heavy Metal Concentration: {pred_metal:.4f} mg/L")
print(f"Bacterial Contamination: {'Contaminated' if pred_bacteria == 1 else 'Safe'}")
