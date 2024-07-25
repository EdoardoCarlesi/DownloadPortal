import json
import os
#from paypalhttp import HttpClient, SandboxEnvironment
from paypalhttp import HttpClient, Environment
from paypalhttp.serializers.json_serializer import Json
from paypalhttp.http_error import HttpError
#from paypalhttp.payments import OrdersCreateRequest, OrdersCaptureRequest

# Set up PayPal client
client_id = os.getenv('PAYPAL_ID')
client_secret = os.getenv('PAYPAL_SECRET')
environment = Environment("http://www.nanowar.it") #client_id=client_id, client_secret=client_secret)
client = HttpClient(environment)

# Create function to initiate payment
def initiate_payment(amount):
    request = OrdersCreateRequest()
    request.prefer('return=representation')
    request.request_body({
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": amount
            }
        }]
    })

    try:
        response = client.execute(request)
        return response.result.id
    except HttpError as e:
        print(e.status_code)
        print(e.headers)
        print(json.loads(e.message))
        raise

# Create function to verify payment
def verify_payment(order_id):
    request = OrdersCaptureRequest(order_id)

    try:
        response = client.execute(request)
        return response.result.status == 'COMPLETED'
    except HttpError as e:
        print(e.status_code)
        print(e.headers)
        print(json.loads(e.message))
        return False

# Flask route to handle payment initiation
@app.route('/initiate-payment', methods=['POST'])
def initiate_payment_route():
    amount = request.json['amount']
    try:
        order_id = initiate_payment(amount)
        return {'orderId': order_id}, 200
    except:
        return {'error': 'Failed to initiate payment'}, 500

# Flask route to handle payment verification
@app.route('/verify-payment', methods=['POST'])
def verify_payment_route():
    order_id = request.json['orderId']
    try:
        is_verified = verify_payment(order_id)
        if is_verified:
            code = generate_code() # Implement your code generation logic
            return {'code': code}, 200
        else:
            return {'error': 'Payment verification failed'}, 400
    except:
        return {'error': 'Failed to verify payment'}, 500

