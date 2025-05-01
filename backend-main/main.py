import os
import numpy as np
import joblib
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import gspread
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Load .env
load_dotenv()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
INPUT_SHEET_NAME = os.getenv("INPUT_SHEET_NAME")
OUTPUT_SHEET_NAME = os.getenv("OUTPUT_SHEET_NAME")

# Load models
bacteria_model = joblib.load("models/bacteria_model.pkl")
do_model = joblib.load("models/do_model.pkl")
metal_model = joblib.load("models/metal_model.pkl")
scaler = joblib.load("models/scaler.pkl")

# Setup Google Sheets Auth
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
def get_gspread_client():
    creds = None
    if os.path.exists("sheets_auth/token.json"):
        creds = Credentials.from_authorized_user_file("sheets_auth/token.json", SCOPES)
    else: raise RuntimeError("token.json not found. Please generate it locally using flow.run_local_server.")
    return gspread.authorize(creds)

gc = get_gspread_client()
sheet = gc.open_by_key(SPREADSHEET_ID)
input_ws = sheet.worksheet(INPUT_SHEET_NAME)
output_ws = sheet.worksheet(OUTPUT_SHEET_NAME)

# Initialize FastAPI
app = FastAPI(title="Water Quality Predictor (Google Sheets Edition)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/predict")
def predict_water_quality():
    rows = input_ws.get_all_records()
    if not rows:
        return {"error": "No sensor data found in the input sheet."}
    
    last_entry = rows[-1]
    temperature = float(last_entry["temperature"])
    ph = float(last_entry["ph"])
    tds = float(last_entry["tds"])
    turbidity = float(last_entry["turbidity"])

    # Preprocessing
    input_data = np.array([[temperature, ph, tds, turbidity]])
    input_scaled = scaler.transform(input_data)

    # Predict
    pred_bacteria = bacteria_model.predict(input_scaled)[0]
    pred_do = do_model.predict(input_scaled)[0]
    pred_metal = metal_model.predict(input_scaled)[0]

    # Evaluate suitability
    is_suitable = (
        6.5 <= ph <= 8.5 and
        tds <= 500 and
        turbidity <= 5 and
        pred_do >= 5 and
        pred_metal < 0.0115 and
        pred_bacteria == 0
    )
    water_status = "Suitable for Drinking" if is_suitable else "Not Suitable for Drinking"
    bacterial_status = "Contaminated" if pred_bacteria == 1 else "Safe"

    # Append to output sheet
    output_ws.append_row([
        temperature, ph, tds, turbidity,
        f"{pred_do:.2f} mg/L",
        f"{pred_metal:.4f} mg/L",
        bacterial_status,
        water_status
    ])

    return {
        "temperature": temperature,
        "ph": ph,
        "tds": tds,
        "turbidity": turbidity,
        "Dissolved Oxygen (DO)": f"{pred_do:.2f} mg/L",
        "Heavy Metal Concentration": f"{pred_metal:.4f} mg/L",
        "Bacterial Contamination": bacterial_status,
        "Water Suitability": water_status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
