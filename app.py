import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler

# Load the trained model 
model = joblib.load('model/linear_reg_model.joblib')
scaler = MinMaxScaler()

# Define the UI elements
st.title('House Price Prediction App')

# Input features
#NICE TO HAVE - sliders for the inputs, dropdowns for the categorical inputs, essential inputs handled + validation for inputs

area_input = st.number_input("How large should the area of the property be?")
bedrooms_input = st.number_input("How many bedrooms should the property have?")
bathrooms_input = st.number_input("How many bathrooms should the property have?")
stories_input = st.number_input("How many stories should the property have?")
parking_input = st.number_input("How much parking space should the property have?")
mainroad_input = st.selectbox("Do you wish the property to be by the main road?", ("Yes", "No")) #Need to handle this
guestroom_input = st.selectbox("Do you wish to have a guest room?", ("Yes", "No")) #Need to handle this
basement_input = st.selectbox("Do you wish to have a guest basement?", ("Yes", "No")) #Need to handle this
hotwaterheating_input = st.selectbox("Do you wish to have a hot water?", ("Yes", "No")) #Need to handle this
airconditioning_input = st.selectbox("Do you prefer AC rooms?", ("Yes", "No")) #Need to handle this
furnishingstatus_input = st.selectbox("How should the furnishing status be?", ("Furnished", "Semi-Furnished", "Unfurnished")) #Need to handle this

# Preprocess the inputs
if mainroad_input == "Yes":
    mainroad_no = 0
    mainroad_yes = 1
elif mainroad_input == "No":
    mainroad_no = 1
    mainroad_yes = 0

if guestroom_input == "Yes":
    guestroom_no = 0
    guestroom_yes = 1
elif guestroom_input == "No":
    guestroom_no = 1
    guestroom_yes = 0

if basement_input == "Yes":
    basement_no = 0
    basement_yes = 1
elif basement_input == "No":
    basement_no = 1
    basement_yes = 0

if hotwaterheating_input == "Yes":
    hotwaterheating_no = 0
    hotwaterheating_yes = 1
elif hotwaterheating_input == "No":
    hotwaterheating_no = 1
    hotwaterheating_yes = 0

if airconditioning_input == "Yes":
    airconditioning_no = 0
    airconditioning_yes = 1
elif airconditioning_input == "No":
    airconditioning_no = 1
    airconditioning_yes = 0

if furnishingstatus_input == "Furnished":
    furnishingstatus_furnished = 1
    furnishingstatus_semi_furnished = 0
    furnishingstatus_unfurnished = 0
elif furnishingstatus_input == "Semi-Furnished":
    furnishingstatus_furnished = 0
    furnishingstatus_semi_furnished = 1
    furnishingstatus_unfurnished = 0
elif furnishingstatus_input == "Unfurnished":
    furnishingstatus_furnished = 0
    furnishingstatus_semi_furnished = 0
    furnishingstatus_unfurnished = 1

# Dataset documentation does not specify what the pref_area is, so we will assume 1 for all inputs    
prefarea_no = 0
prefarea_yes = 1

data = {
    'area': area_input,
    'bedrooms': bedrooms_input,
    'bathrooms': bathrooms_input,
    'stories': stories_input,
    'parking': parking_input,
    'mainroad_no': mainroad_no,
    'mainroad_yes': mainroad_yes,
    'guestroom_no': guestroom_no,
    'guestroom_yes': guestroom_yes,
    'basement_no': basement_no,
    'basement_yes': basement_yes,
    'hotwaterheating_no': hotwaterheating_no,
    'hotwaterheating_yes': hotwaterheating_yes,
    'airconditioning_no': airconditioning_no,
    'airconditioning_yes': airconditioning_yes,
    'prefarea_no': prefarea_no,
    'prefarea_yes': prefarea_yes,
    'furnishingstatus_furnished': furnishingstatus_furnished,
    'furnishingstatus_semi-furnished': furnishingstatus_semi_furnished,
    'furnishingstatus_unfurnished': furnishingstatus_unfurnished
}

df_unseen = pd.DataFrame([data])
# BETTER OPTION - scale the unseen data with the scaler used for the training data (MinMaxScaler - should be saved with the model)

# Make predictions with Predict button
if st.button("Predict"):
    prediction = model.predict(df_unseen)
    print(prediction)
    st.write(f"Predicted House Price: ${prediction[0]}")