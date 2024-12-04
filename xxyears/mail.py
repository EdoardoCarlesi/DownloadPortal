import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def sendconfirmation(to : str, password : str, code : str):

    # Send email with album code
    smtp_server = 'smtp.xxyearsofsteel.com'
    smtp_port = 587
    smtp_username = os.environ.get('SMTP_USERNAME_INFO')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    site_url = 'www.xxyearsofsteel.com/login'

    msg = MIMEMultipart()
    msg['From'] = 'info@xxyearsofsteel.com'
    msg['To'] = to
    msg['Subject'] = "XX Years Of Steel - Video Portal Registration Successful!"

    message_text = f"""
 Thanks for registering on www.xxyearsofsteel.com with the code: {code} 

 Your mail is also your username, while your password is: {password} 

 You can then access the XX Years Of Steel video entering the (incredible) video section of the website, where 
 you will find some download links. The download links change regularly so make sure you download the videos as soon
 as you log in, and in case one of them does not work try to refresh the page or log out & log in again.

 Enjoy the show! 

                    - Yours truly, Nanowar Of Steel

DISCLAIMER:

This portal was completely developed by me (Gatto Panceri 666), so please bear with all the ugly graphics and bugs.
I will spare you all the details about how painful and costly was to record and edit this video and audio, which is the
reason why we relied on a "in house"-developed platform of this kind was mainly to avoid all the high fees 
that other services require. 
I also wanted to start developing something which in the future might be helpful to distribute some 
other exclusive Nanowar Of Steel content as well.

For the moment, I apologize in advance for any inconvenience - rest assured I will be there and try to help in case any problem should emerge!

                - Gatto
    """

    msg.attach(MIMEText(message_text, 'plain')) 

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)


def sendmail(to : str, subject : str, code : str):

    # Send email with album code
    smtp_server = 'smtp.xxyearsofsteel.com'
    smtp_port = 587
    smtp_username = os.environ.get('SMTP_USERNAME_INFO')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    site_url = 'www.xxyearsofsteel.com/login'

    msg = MIMEMultipart()
    msg['From'] = 'info@xxyearsofsteel.com'
    msg['To'] = to
    msg['Subject'] = subject

    message_text = f"""
 Thanks for your purchase!

 You can now register on: 
 {site_url} 

 using the code: 
 {code} 

 You can now register on the XX Years Of Steel portal using this code.

 That's moderately amazing! 

                    - Yours truly, Nanowar Of Steel

DISCLAIMER:

This portal was completely developed by me (Gatto Panceri 666), so please bear with all the ugly graphics and bugs.
I will spare you all the details about how painful and costly was to record and edit this video and audio, which is the
reason why we relied on a "in house"-developed platform of this kind was mainly to avoid all the high fees 
that other services require. 
I also wanted to start developing something which in the future might be helpful to distribute some 
other exclusive Nanowar Of Steel content as well.

For the moment, I apologize in advance for any inconvenience - rest assured I will be there and try to help in case any problem should emerge!

                - Gatto
    """

    msg.attach(MIMEText(message_text, 'plain')) 

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)


def send_report(mail_to='gatto@nanowar.it', subject='Video Stream Monthly Report', attach='tmp/report.pdf'):

    # Send email with sales report attached
    smtp_server = 'smtp.xxyearsofsteel.com'
    smtp_port = 587
    smtp_username = os.environ.get('SMTP_USERNAME_SALES')
    smtp_password = os.environ.get('SMTP_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = 'sales@xxyearsofsteel.com'
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

