from flask import Flask, request, jsonify
# from model import predict_price  # Giả sử bạn có một hàm dự đoán trong mô-đun 'model'
import joblib
import json
import pandas as pd
from babel.numbers import format_currency

def convert_to_currency(number, currency='VND'):
    return format_currency(number, currency, locale='vi_VN')

app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    model = joblib.load('models/rf.pkl')


    with open('mapping.json', 'r') as file:
        mapping = json.load(file)

    data = request.get_json()  # Lấy dữ liệu từ yêu cầu POST

    # Concatenate the values into a DataFrame
    df = pd.DataFrame({
        'manufacture_date': [mapping['manufacture_date'][str(data.get('manufacture_date'))]],
        'brand': [mapping['brand'][data.get('brand')]],
        'model': [mapping['model'][data.get('model')]],
        'origin': [mapping['origin'][data.get('origin')]],
        'type': [mapping['type'][data.get('type')]],
        'seats': [mapping['seats'][str(data.get('seats'))]],
        'gearbox': [mapping['gearbox'][data.get('gearbox')]],
        'fuel': [mapping['fuel'][data.get('fuel')]],
        'color': [mapping['color'][data.get('color')]],
        'mileage_v2': [data.get('mileage_v2')]
        
    })

    # Use the model to make a prediction
    prediction = model.predict(df)

    output = convert_to_currency(prediction[0])
    return jsonify({'prediction': output})

if __name__ == '__main__':
    app.run(debug=True)
