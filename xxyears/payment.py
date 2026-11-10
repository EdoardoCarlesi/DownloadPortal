from flask import (Blueprint, redirect, render_template, url_for, jsonify, session)
from requests.auth import HTTPBasicAuth
import requests
import os, json, re
import xxyears.codes as codes
import xxyears.mail as mail

bp = Blueprint('payment', __name__, url_prefix='/payment')

#PAYPAL_BUSINESS_CLIENT_ID = os.getenv("PAYPAL_SANDBOX_ID")
#PAYPAL_BUSINESS_SECRET = os.getenv("PAYPAL_SANDBOX_PW")
#PAYPAL_API_URL = f"https://api-m.sandbox.paypal.com"

credentials_file = 'json/.paypal_credentials.json'
PAYPAL_BUSINESS_CLIENT_ID = os.getenv("PAYPAL_ID")
PAYPAL_BUSINESS_SECRET = os.getenv("PAYPAL_PW")
PAYPAL_API_URL = "https://api-m.paypal.com"

if not PAYPAL_BUSINESS_CLIENT_ID or not PAYPAL_BUSINESS_SECRET:
    try:
        with open(credentials_file, 'r') as file:
            credentials = json.load(file)
            PAYPAL_BUSINESS_CLIENT_ID = credentials.get("PAYPAL_ID", "").strip()
            PAYPAL_BUSINESS_SECRET = credentials.get("PAYPAL_PW", "").strip()
    except (FileNotFoundError, json.JSONDecodeError):
        raise RuntimeError(
            f"Missing or invalid PayPal credentials! Ensure either environment variables are properly set or '{credentials_file}' contains valid data.")

paypal_id=f"https://www.paypal.com/sdk/js?client-id={PAYPAL_BUSINESS_CLIENT_ID}&currency=EUR"

# Must match the amount set in templates/payment/payment.html.
EXPECTED_AMOUNT = '4.99'
EXPECTED_CURRENCY = 'EUR'
ORDER_ID_RE = re.compile(r'^[A-Za-z0-9]{1,64}$')

@bp.route('/payment', methods=['POST'])
def payment():
    print('paypal_id: ', paypal_id)
    return render_template('payment/payment.html', paypal_id=paypal_id)

@bp.route("/<order_id>/capture", methods=["POST"])
def capture_payment(order_id):  # Checks and confirms payment
    if not ORDER_ID_RE.match(order_id):
        return jsonify({'error': 'Invalid order id'}), 400

    captured_payment = paypal_capture_function(order_id)

    if is_approved_payment(captured_payment):
        mail_to = captured_payment['payment_source']['paypal']['email_address']
        code_bought = codes.reserve_sell_code(mail_to)
        if not code_bought:
            # The buyer has been charged; this needs a manual refund.
            print(f"NO SELL CODES LEFT: order {order_id} from {mail_to} was paid but got no code.")
            return jsonify({'error': 'No codes available'}), 500
        try:
            mail.send_code(to=mail_to, subject='XX Years of Steel Video Code', code=code_bought)
        except Exception as e:
            print(f"There was an error sending your confirmation mail: {e}")
        # Kept in the buyer's own session only, never in a shared file or in the response.
        session['purchase'] = {'code': code_bought}
        return jsonify(captured_payment)
    else:
        return jsonify({'error': 'Payment not approved'}), 400

def paypal_capture_function(order_id):
    post_route = f"/v2/checkout/orders/{order_id}/capture"
    paypal_capture_url = PAYPAL_API_URL + post_route
    basic_auth = HTTPBasicAuth(PAYPAL_BUSINESS_CLIENT_ID, PAYPAL_BUSINESS_SECRET)
    headers = {
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(url=paypal_capture_url, headers=headers, auth=basic_auth, timeout=15)
        response.raise_for_status()
        json_data = response.json()
        return json_data
    except requests.RequestException as e:
        print(f"Error during PayPal capture request: {e}")
        return {}

@bp.route('/success') 
def success():
    purchase = session.pop('purchase', None)
    if not purchase:
        return redirect(url_for("payment.payment"))

    return render_template('payment/success.html', code=purchase['code'])


def is_approved_payment(captured_payment):
    if not captured_payment or captured_payment.get("status") != "COMPLETED":
        return False

    try:
        capture = captured_payment["purchase_units"][0]["payments"]["captures"][0]
        amount = capture["amount"]
        return (capture.get("status") == "COMPLETED"
                and amount["value"] == EXPECTED_AMOUNT
                and amount["currency_code"] == EXPECTED_CURRENCY
                and bool(captured_payment["payment_source"]["paypal"]["email_address"]))
    except (KeyError, IndexError, TypeError):
        return False

