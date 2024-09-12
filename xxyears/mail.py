import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendmail(to : str, subject : str, code : str):

    # Send email with album code
    smtp_server = 'smtp.xxyearsofsteel.com'
    smtp_port = 587
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    site_url = 'www.xxyearsofsteel.com/login'

    msg = MIMEMultipart()
    msg['From'] = 'password-reset@xxyearsofsteel.com'
    msg['To'] = to
    msg['Subject'] = subject
    message_text = f'\n Thanks for your purchase!\n\n You can now register on: \n {site_url} \n\n using the code: \n {code} \n\n Enjoy the show!'
    msg.attach(MIMEText(message_text, 'plain')) 

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)


def send_report(mail_to='gatto@nanowar.it', subject='Video Stream Monthly Report', attach='tmp/report.pdf'):

    # Send email with sales report attached
    smtp_server = 'smtp.xxyearsofsteel.com'
    smtp_port = 587
    smtp_username = os.environ.get('SMTP_USERNAME')
    smtp_password = os.environ.get('SMTP_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = 'password-reset@xxyearsofsteel.com'
    msg['To'] = mail_to
    msg['Subject'] = subject
    message_text = f'{header}\n '
    msg.attach(MIMEText(message_text, 'plain')) 
    #f'Click the following link to reset your password: {reset_link}', 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)


if __name__ == '__main__':
    sendmail(to='gatto@nanowar.it', subject='XX Years Code', code='dummy-test-666')

