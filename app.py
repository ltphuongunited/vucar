import streamlit as st
import requests
import json 


# Flask app API URL
API_URL = 'http://127.0.0.1:5000/predict'


with open('mapping.json', 'r') as file:
    mapping = json.load(file)

features = {}

for key in mapping:
    features[key] = list(mapping[key].keys())

st.title('Car Price Prediction App')
st.subheader('Enter car features to predict the price')

brand = st.selectbox('Brand', features['brand'])
model = st.selectbox('Model', features['model'])
origin = st.selectbox('Origin', features['origin'])
car_type = st.selectbox('Car Type', features['type'])
seats = st.selectbox('Number of Seats', features['seats'])
gearbox = st.selectbox('Gearbox', features['gearbox'])
fuel = st.selectbox('Fuel', features['fuel'])
color = st.selectbox('Color', features['color'])
mileage = st.number_input('Mileage (in km)', min_value=0.0, max_value=1e9)
manufacture_date = st.selectbox('Manufacture date', features['manufacture_date'])

# Prediction button
if st.button('Predict'):
    # Send POST request to the API for price prediction
    data = {
        'brand': brand,
        'model': model,
        'origin': origin,
        'type': car_type,
        'seats': seats,
        'gearbox': gearbox,
        'fuel': fuel,
        'color': color,
        'mileage_v2': mileage,
        "manufacture_date": manufacture_date
    }

    response = requests.post(API_URL, json=data)
    prediction = response.json()['prediction']

    # Display the prediction result
    st.subheader('Prediction Result')
    st.write(f'Predicted Price: {prediction}')
