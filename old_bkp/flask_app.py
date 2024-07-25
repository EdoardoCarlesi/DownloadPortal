import flask
from requests.auth import HTTPBasicAuth
import os

app = flask.Flask(__name__)

# # # # PAYPAL SANDBOX
PAYPAL_BUSINESS_CLIENT_ID = os.getenv("PAYPAL_ID")
PAYPAL_BUSINESS_SECRET = os.getenv("PAYPAL_SECRET")
PAYPAL_API_URL = f"https://api-m.sandbox.paypal.com"
 
# # # # PAYPAL LIVE Details
# PAYPAL_BUSINESS_CLIENT_ID = os.getenv("PAYPAL_LIVE_BUSINESS_CLIENT_ID")
# PAYPAL_BUSINESS_SECRET = os.getenv("PAYPAL_LIVE_BUSINESS_SECRET")
# PAYPAL_API_URL = f"https://api-m.paypal.com"
 
# PAYPAL payment price
IB_TAX_APP_PRICE = float(3.99)
IB_TAX_APP_PRICE_CURRENCY = "EUR"
 
@app.route("/payment")
#@login_required
def paypal_payment():
    return render_template("payment.html", paypal_business_client_id=PAYPAL_BUSINESS_CLIENT_ID,
                           price=IB_TAX_APP_PRICE, currency=IB_TAX_APP_PRICE_CURRENCY)
 
@app.route("/payment/<order_id>/capture", methods=["POST"])
def capture_payment(order_id):  # Checks and confirms payment
    captured_payment = paypal_capture_function(order_id)
    # print(captured_payment)
    #if is_approved_payment(captured_payment):
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

if __name__ == '__main__':

    pass

