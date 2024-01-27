import streamlit as st
import pandas as pd
import joblib
import locale

# Load the trained model 
model = joblib.load('model/linear_reg_model.joblib')
scaler = joblib.load('model/scaler.joblib')
locale.setlocale( locale.LC_ALL, '' )

# Define the UI elements
st.markdown("<h1 style='text-align: center;'>Luxury House Price Prediction 🏘️</h1>", unsafe_allow_html=True)

# Input features
# INCLUDES: +/- for each input, validation checks, min/max values, dropdowns, etc.
area_input = st.number_input("How large should the area of the property be?", min_value=1000, max_value=16500, step=500)
bedrooms_input = st.number_input("How many bedrooms should the property have?", min_value=1, max_value=10, step=1)
bathrooms_input = st.number_input("How many bathrooms should the property have?", min_value=1, max_value=5, step=1)
stories_input = st.number_input("How many stories should the property have?", min_value=1, max_value=4, step=1)
parking_input = st.number_input("How much parking space should the property have?", min_value=0, max_value=4, step=1)
mainroad_input = st.selectbox("Do you wish the property to be by the main road?", ("Yes", "No")) #Need to handle this
guestroom_input = st.selectbox("Do you wish to have a guest room?", ("Yes", "No")) #Need to handle this
basement_input = st.selectbox("Do you wish to have a guest basement?", ("Yes", "No")) #Need to handle this
hotwaterheating_input = st.selectbox("Do you wish to have a hot water?", ("Yes", "No")) #Need to handle this
airconditioning_input = st.selectbox("Do you prefer AC rooms?", ("Yes", "No")) #Need to handle this
furnishingstatus_input = st.selectbox("How should the furnishing status be?", ("Furnished", "Semi-Furnished", "Unfurnished")) #Need to handle this

# Function to preprocess binary inputs
def preprocess_binary_input(input_value):
    if input_value == "Yes":
        return 0, 1
    else:
        return 1, 0
    
# Function to preprocess furnished inputs
def preprocess_furnished_input(input_value):
    if input_value == "Furnished":
        return 1, 0, 0
    elif input_value == "Semi-Furnished":
        return 0, 1, 0
    else:
        return 0, 0, 1

#Function to process the input features and return the scaled inputs in a dataframe
def processFeatures(area_input, bedrooms_input, bathrooms_input, stories_input, parking_input, mainroad_no, mainroad_yes, guestroom_no, guestroom_yes, basement_no, basement_yes, hotwaterheating_no, hotwaterheating_yes, airconditioning_no, airconditioning_yes, prefarea_no, prefarea_yes, furnishingstatus_furnished, furnishingstatus_semi_furnished, furnishingstatus_unfurnished):
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
    # Create a dataframe with the inputs and scale them
    df_input_data = pd.DataFrame([data])
    input_scaled_data = scaler.transform(df_input_data)
    return input_scaled_data

# Preprocess the inputs
mainroad_no, mainroad_yes = preprocess_binary_input(mainroad_input)
guestroom_no, guestroom_yes = preprocess_binary_input(guestroom_input)
basement_no, basement_yes = preprocess_binary_input(basement_input)
hotwaterheating_no, hotwaterheating_yes = preprocess_binary_input(hotwaterheating_input)
airconditioning_no, airconditioning_yes = preprocess_binary_input(airconditioning_input)

# Dataset documentation does not specify what the pref_area is, so we will assume 1 for all inputs    
prefarea_no = 0
prefarea_yes = 1

# Preprocess the furnished inputs
furnishingstatus_furnished, furnishingstatus_semi_furnished, furnishingstatus_unfurnished = preprocess_furnished_input(furnishingstatus_input)

#Call the function to process the inputs
input_scaled_data = processFeatures(area_input, bedrooms_input, bathrooms_input, stories_input, parking_input, mainroad_no, mainroad_yes, guestroom_no, guestroom_yes, basement_no, basement_yes, hotwaterheating_no, hotwaterheating_yes, airconditioning_no, airconditioning_yes, prefarea_no, prefarea_yes, furnishingstatus_furnished, furnishingstatus_semi_furnished, furnishingstatus_unfurnished)

# Make predictions with Predict button
if st.button("Predict price"):
    prediction = model.predict(input_scaled_data)
    prediction = round(prediction[0], 2)
    cost = locale.currency(prediction, grouping=True)
    # st.write(f"Predicted House Price: {cost}")

    st.markdown(f"<h1 style='text-align: center; color: white;'>Predicted House Price</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color: white;'>{cost}</h2>", unsafe_allow_html=True)