import streamlit as st
import pickle

# Load model
with open('waterml.pkl', 'rb') as f:
    model = pickle.load(f)

# UI
st.title("Water Intake Predictor")
st.write("Predict your daily water requirement based on age and gender.")

# Input 
age = st.slider("Select your age:", 10, 80, 25)
gender = st.radio("Select your gender:", ("Female", "Male"))

# Map gender to 0/1
gender_value = 0 if gender == "Female" else 1

# Prediction button
if st.button("Predict"):
    prediction = model.predict([[age, gender_value]])
    st.success(f"Recommended Daily Water Intake: {prediction[0]:.2f} liters")

#REDIRECT ON REMINDER PAGE
if st.button("Set Reminder"):
    st.switch_page("pages/reminder.py")
