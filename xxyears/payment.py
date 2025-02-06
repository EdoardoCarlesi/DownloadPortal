from flask import (Blueprint, flash, redirect, render_template, url_for, jsonify)
from requests.auth import HTTPBasicAuth
import requests
import os
import xxyears.codes as codes
import xxyears.mail as mail
import pickle as pkl

bp = Blueprint('payment', __name__, url_prefix='/payment')

#PAYPAL_BUSINESS_CLIENT_ID = os.getenv("PAYPAL_SANDBOX_ID")
#PAYPAL_BUSINESS_SECRET = os.getenv("PAYPAL_SANDBOX_PW")
#PAYPAL_API_URL = f"https://api-m.sandbox.paypal.com"
PAYPAL_BUSINESS_CLIENT_ID = os.getenv("PAYPAL_ID")
PAYPAL_BUSINESS_SECRET = os.getenv("PAYPAL_PW")
PAYPAL_API_URL = "https://api-m.{env}.paypal.com".format(env="paypal")

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
    try:
        with open(tmp_captured, 'rb') as temp_file:
            captured_payment = pkl.load(temp_file)
    
        mail_to = captured_payment["payment_source"]["paypal"]["email_address"]
        video_code = captured_payment["code_video"]
    
        try:
            mail.send_code(to=mail_to, subject='XX Years of Steel Video Code', code=video_code)
        except Exception as e:
            print(f"There was an error sending your confirmation mail: {e}")
    
        os.remove(tmp_captured)
        return render_template('payment/success.html', code=video_code)
    except FileNotFoundError:
        print("Temporary capture file not found.")
        return redirect(url_for("payment.payment"))

def is_approved_payment(captured_payment):
    status = captured_payment.get("status")
    payment_source = captured_payment["payment_source"]["paypal"]
    payment_unit = captured_payment.get("purchase_units", [{}])[0]
    capture_details = payment_unit.get("payments", {}).get("captures", [{}])[0]
    
    email = payment_source.get("email_address")
    amount = capture_details.get("amount", {}).get("value")
    currency_code = capture_details.get("amount", {}).get("currency_code")
    
    return status == "COMPLETED"

