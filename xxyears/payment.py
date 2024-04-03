import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from requests.auth import HTTPBasicAuth
import requests
import os

bp = Blueprint('payment', __name__, url_prefix='/payment')

PAYPAL_BUSINESS_CLIENT_ID = os.getenv("PAYPAL_SANDBOX_ID")
PAYPAL_BUSINESS_SECRET = os.getenv("PAYPAL_SANDBOX_PW")
PAYPAL_API_URL = f"https://api-m.sandbox.paypal.com"

paypal_id=f"https://www.paypal.com/sdk/js?client-id={PAYPAL_BUSINESS_CLIENT_ID}&currency=EUR"

@bp.route('/payment', methods=['POST'])
def payment():
    return render_template('payment/payment.html', paypal_id=paypal_id)

@bp.route("/<order_id>/capture", methods=["POST"])
def capture_payment(order_id):  # Checks and confirms payment
    print('order id: ', order_id)
    captured_payment = paypal_capture_function(order_id)
    
    if is_approved_payment(captured_payment):
        flash("Payment approved")
        flash("Your code is: cazzo-di-cane-6789")
        return redirect(url_for('payment.success'))
        #return jsonify(captured_payment)
    else:
        flash("Payment not approved!")
        # generate some wrong order page 
    
    #return render_template('payment/success.html')
    #return render_template('payment/payment.html', paypal_id=paypal_id)
    
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
    
@bp.route('/success', methods=['GET'])
def success():
    print('Payment successful!')
    return render_template('payment/success.html')


def is_approved_payment(captured_payment):
    status = captured_payment.get("status")
    print(captured_payment)
    email = captured_payment["payment_source"]["paypal"]["email_address"]
    amount = captured_payment.get("purchase_units")[0].get("payments").get("captures")[0].get("amount").get("value")
    currency_code = captured_payment.get("purchase_units")[0].get("payments").get("captures")[0].get("amount").get(
        "currency_code")
    print(f"Payment happened. Details: {status}, {amount}, {currency_code}, {email}")
    if status == "COMPLETED":
        return True
    else:
        return False

