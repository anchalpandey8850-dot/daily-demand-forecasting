
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(BASE_DIR / "final_linear_regression_model.pkl")
features = joblib.load(BASE_DIR / "final_model_features.pkl")

app = FastAPI(
    title="Daily Demand Forecasting API",
    description="Predict total orders using a trained Linear Regression model.",
    version="1.0.0"
)

class OrderInput(BaseModel):
    week_of_month: int = Field(ge=1, le=5)
    day_of_week: int = Field(ge=1, le=5)
    non_urgent_order: float = Field(ge=0)
    urgent_order: float = Field(ge=0)
    fiscal_sector_orders: float = Field(ge=0)
    traffic_controller_orders: float = Field(ge=0)
    banking_orders_1: float = Field(ge=0)
    banking_orders_2: float = Field(ge=0)
    banking_orders_3: float = Field(ge=0)

@app.get("/")
def home():
    return {"message": "Daily Demand Forecasting API is running"}

@app.get("/features")
def get_features():
    return {"features": features}

@app.post("/predict")
def predict_orders(data: OrderInput):
    try:
        input_values = {
            features[0]: data.week_of_month,
            features[1]: data.day_of_week,
            features[2]: data.non_urgent_order,
            features[3]: data.urgent_order,
            features[4]: data.fiscal_sector_orders,
            features[5]: data.traffic_controller_orders,
            features[6]: data.banking_orders_1,
            features[7]: data.banking_orders_2,
            features[8]: data.banking_orders_3,
        }

        input_df = pd.DataFrame([input_values], columns=features)
        prediction = float(model.predict(input_df)[0])

        return {"predicted_total_orders": round(prediction, 2)}

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
