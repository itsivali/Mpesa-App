from flask import Flask, render_template, request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import base64

app = Flask(__name__)

# M-Pesa credentials
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
shortcode = 'YOUR_SHORTCODE'
lipa_na_mpesa_online_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
passkey = 'YOUR_PASSKEY'

# Function to get access token
def get_access_token():
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    if response.status_code == 200:
        return json.loads(response.text)['access_token']
    else:
        return None

# Function to generate password
def generate_password():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password_str = f'{shortcode}{passkey}{timestamp}'
    password = base64.b64encode(password_str.encode()).decode('utf-8')
    return password, timestamp

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pay', methods=['POST'])
def pay():
    phone_number = request.form['phone']
    amount = request.form['amount']
    access_token = get_access_token()

    if not access_token:
        return jsonify({"error": "Failed to get access token"}), 400

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    password, timestamp = generate_password()

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://yourcallbackurl.com/callback",
        "AccountReference": "Test123",
        "TransactionDesc": "Payment"
    }

    response = requests.post(lipa_na_mpesa_online_url, json=payload, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to process payment"}), 400

if __name__ == '__main__':
    app.run(debug=True)
