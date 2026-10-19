
import requests
import streamlit as st

API_URL = "https://daily-demand-forecasting-1.onrender.com/predict"
st.set_page_config(
    page_title="Daily Demand Forecasting",
    page_icon="📦",
    layout="centered"
)

st.title("📦 Daily Demand Forecasting")
st.write("Enter order details to predict total orders.")

with st.form("forecast_form"):
    week_of_month = st.number_input(
        "Week of the month", min_value=1, max_value=5, value=2
    )
    day_of_week = st.number_input(
        "Day of the week (Monday=1 to Friday=5)",
        min_value=1, max_value=5, value=3
    )

    non_urgent_order = st.number_input(
        "Non-urgent orders", min_value=0.0, value=100.0
    )
    urgent_order = st.number_input(
        "Urgent orders", min_value=0.0, value=50.0
    )
    fiscal_sector_orders = st.number_input(
        "Fiscal sector orders", min_value=0.0, value=30.0
    )
    traffic_controller_orders = st.number_input(
        "Traffic controller sector orders", min_value=0.0, value=20.0
    )
    banking_orders_1 = st.number_input(
        "Banking orders (1)", min_value=0.0, value=10.0
    )
    banking_orders_2 = st.number_input(
        "Banking orders (2)", min_value=0.0, value=15.0
    )
    banking_orders_3 = st.number_input(
        "Banking orders (3)", min_value=0.0, value=5.0
    )

    submitted = st.form_submit_button("Predict Total Orders")

if submitted:
    payload = {
        "week_of_month": int(week_of_month),
        "day_of_week": int(day_of_week),
        "non_urgent_order": non_urgent_order,
        "urgent_order": urgent_order,
        "fiscal_sector_orders": fiscal_sector_orders,
        "traffic_controller_orders": traffic_controller_orders,
        "banking_orders_1": banking_orders_1,
        "banking_orders_2": banking_orders_2,
        "banking_orders_3": banking_orders_3
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()
        prediction = response.json()["predicted_total_orders"]

        if prediction < 0:
            st.warning(
                f"Model returned {prediction:.2f}. "
                "A negative order count is not meaningful. "
                "Review the input values and model performance."
            )
        else:
            st.success(f"Predicted Total Orders: {prediction:.2f}")

    except requests.exceptions.RequestException as error:
        st.error(
            "Could not connect to the forecasting API. "
            "Make sure FastAPI is running on port 8002."
        )
        st.caption(str(error))
