import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from requests.auth import HTTPBasicAuth
import requests
import os
from . import codes
from . import mail
import pickle as pkl

bp = Blueprint('payment', __name__, url_prefix='/payment')

PAYPAL_BUSINESS_CLIENT_ID = os.getenv("PAYPAL_SANDBOX_ID")
PAYPAL_BUSINESS_SECRET = os.getenv("PAYPAL_SANDBOX_PW")
PAYPAL_API_URL = f"https://api-m.sandbox.paypal.com"
paypal_id=f"https://www.paypal.com/sdk/js?client-id={PAYPAL_BUSINESS_CLIENT_ID}&currency=EUR"
tmp_captured = 'captured.tmp'

@bp.route('/payment', methods=['POST'])
def payment():
    print('paypal_id: ', paypal_id)
    return render_template('payment/payment.html', paypal_id=paypal_id)

@bp.route("/<order_id>/capture", methods=["POST"])
def capture_payment(order_id):  # Checks and confirms payment
    captured_payment = paypal_capture_function(order_id)
    
    if is_approved_payment(captured_payment):
        code_bought = codes.draw_random_sell_code()
        captured_payment['code_video'] = code_bought
        codes.remove_code_from_list(code_bought)
        pkl.dump(captured_payment, open(tmp_captured, 'wb'))
        return jsonify(captured_payment)
    else:
        flash("Payment not approved!")
    
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
    
@bp.route('/success') 
def success():
    captured_payment = pkl.load(open(tmp_captured, 'rb'))
    mail_to = captured_payment["payment_source"]["paypal"]["email_address"]
    video_code = captured_payment["code_video"]
    mail.sendmail(mail_to=mail_to, code=video_code)
    os.remove(tmp_captured)
    return render_template('payment/success.html', code=video_code)

def is_approved_payment(captured_payment):
    status = captured_payment.get("status")
    email = captured_payment["payment_source"]["paypal"]["email_address"]
    amount = captured_payment.get("purchase_units")[0].get("payments").get("captures")[0].get("amount").get("value")
    currency_code = captured_payment.get("purchase_units")[0].get("payments").get("captures")[0].get("amount").get(
        "currency_code")
 
    if status == "COMPLETED":
        return True
    else:
        return False

