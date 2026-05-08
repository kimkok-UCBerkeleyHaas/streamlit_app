import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Used Car Price Predictor", layout="wide")
st.title("🚗 What Drives the Price of a Car?")

# Load model
model = joblib.load('used_car_price_model.pkl')

st.sidebar.header("Enter Car Details")

age = st.sidebar.slider("Age of Car (years)", 0, 30, 8)
odometer = st.sidebar.slider("Odometer (miles)", 0, 300000, 60000)
manufacturer = st.sidebar.selectbox("Manufacturer", ["Ford", "Chevrolet", "Toyota", "Honda", ...])  # add your top ones
condition = st.sidebar.selectbox("Condition", ["excellent", "good", "fair", "like new"])
drive = st.sidebar.selectbox("Drive", ["4wd", "fwd", "rwd"])

if st.button("Predict Price"):
    input_data = pd.DataFrame({
        'age': [age],
        'odometer': [odometer],
        # Add other encoded features accordingly
    })
    
    # Note: You need to apply the same preprocessing/dummies as training
    predicted_price = model.predict(input_data)[0]
    st.success(f"**Estimated Market Price: ${predicted_price:,.0f}**")
    