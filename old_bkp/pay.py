import streamlit as st
import requests

# Streamlit app layout
st.title("PayPal Payment Notification")

@st.cache(allow_output_mutation=True)
def get_email_service_api_key():
    # Function to fetch the email service API key
    # In a real-world scenario, this would be securely stored and retrieved
    return 'your_api_key'

def send_email(buyer_email):
    # Replace these variables with your email service credentials and message
    email_service_api_key = get_email_service_api_key()
    sender_email = 'your_email@example.com'
    email_subject = 'Payment Confirmation'
    email_body = 'Your payment has been accepted. Thank you for your purchase!'

    # Send the email using an email service
    # Example using SendGrid
    response = requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        headers={"Authorization": f"Bearer {email_service_api_key}"},
        json={
            "personalizations": [{"to": [{"email": buyer_email}]}],
            "from": {"email": sender_email},
            "subject": email_subject,
            "content": [{"type": "text/plain", "value": email_body}]
        }
    )

    if response.status_code == 202:
        st.success("Email sent successfully")
    else:
        st.error(f"Failed to send email: {response.text}")

# User input for buyer's email
buyer_email = st.text_input("Enter buyer's email:")

# Button to send email
if st.button("Send Email"):
    if buyer_email:
        send_email(buyer_email)
    else:
        st.warning("Please enter a valid email address")
