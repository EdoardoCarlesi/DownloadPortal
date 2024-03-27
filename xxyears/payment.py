import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import os

bp = Blueprint('payment', __name__, url_prefix='/payment')

PAYPAL_BUSINESS_CLIENT_ID = os.getenv("PAYPAL_SANDBOX_ID")
PAYPAL_BUSINESS_SECRET = os.getenv("PAYPAL_SANDBOX_PW")
PAYPAL_API_URL = f"https://api-m.sandbox.paypal.com"

@bp.route('/payment', methods=['POST'])
def payment():
    paypal_id=f"https://www.paypal.com/sdk/js?client-id={PAYPAL_BUSINESS_CLIENT_ID}&currency=EUR"
    return render_template('payment/payment.html', paypal_id=paypal_id)

@bp.route("/payment/<order_id>/capture", methods=["POST"])
def capture_payment(order_id):  # Checks and confirms payment
    captured_payment = paypal_capture_function(order_id)
    print(captured_payment)
    print('Dio Cane Blu')
    if is_approved_payment(captured_payment):
        print('Dio Cane Blu')
        flash("Payment approved")
        flash("Your code is: cazzo-di-cane-6789")
        # Do something (for example Update user field)
    return jsonify(captured_payment)

def paypal_capture_function(order_id):
    post_route = f"/v2/checkout/orders/{order_id}/capture"
    paypal_capture_url = PAYPAL_API_URL + post_route
    basic_auth = HTTPBasicAuth(PAYPAL_BUSINESS_CLIENT_ID, PAYPAL_BUSINESS_SECRET)
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url=paypal_capture_url, headers=headers, auth=basic_auth)
    response.raise_for_status()
    json_data = response.json()
    return json_data

def is_approved_payment(captured_payment):
    status = captured_payment.get("status")
    amount = captured_payment.get("purchase_units")[0].get("payments").get("captures")[0].get("amount").get("value")
    currency_code = captured_payment.get("purchase_units")[0].get("payments").get("captures")[0].get("amount").get(
        "currency_code")
    print(f"Payment happened. Details: {status}, {amount}, {currency_code}")
    if status == "COMPLETED":
        return True
    else:
        return False

