import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import xxyears.video as vid


def send_download_link(to : str, code : str):

    # Send email with album code
    smtp_server = 'smtp.xxyearsofsteel.com'
    smtp_port = 587
    smtp_username = os.environ.get('SMTP_USERNAME_INFO')
    smtp_password = os.environ.get('SMTP_PASSWORD')

    link_part1, link_part2, link_part3 = vid.return_video_urls()

    msg = MIMEMultipart()
    msg['From'] = 'info@xxyearsofsteel.com'
    msg['To'] = to
    msg['Subject'] = "XX Years Of Steel - Video Portal Registration Successful!"
    message_text = f"""
 <br>
 Thanks for redeeming the code: {code} 
 <br>
 You can now download (or stream) the files of the XX Years Of Steel show:
 <br>
 <br>
 <a href={link_part1}>PART 1</a>
 <br>
 <a href={link_part2}>PART 2</a>
 <br>
 <a href={link_part3}>PART 3</a>
 <br>
 <br>
 Enjoy the show! 
 <br>
 <br>
Yours truly, Nanowar Of Steel
 <br>
 <br>
 <br>
 <br>
 <br>
<b>DISCLAIMER:</b>
 <br>
This portal was completely developed by me (Gatto Panceri 666), so please bear with all the ugly graphics and bugs.
 <br>
I will spare you all the details about how painful and costly was to record and edit this video and audio, which is the
reason why we relied on a "in house"-developed platform of this kind was mainly to avoid all the high fees 
that other services require. 
 <br>
 I will also spare you the details on my original project, which was too much to handle in the end, so that I ended up with this easy 
 "get a download link" portal.
 <br>
For the moment, I apologize in advance for any inconvenience - rest assured I will be there and try to help in case any problem should emerge!
 <br>
 <br>
 <br>
Gatto
    """

    msg.attach(MIMEText(message_text, 'html'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)


def send_code(to : str, subject : str, code : str):

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
 Thank you mildly for your purchase!
 <br>
 Use the code: {code} on the <a href="https://www.xxyearsofsteel.com/login">XX Years of Steel website</a> 
 to get a download link for the video files of the XX Years Of Steel show.
<br>
Enjoy!
<br>
<br>
<br>
Yours truly, Nanowar Of Steel
    """

    msg.attach(MIMEText(message_text, 'html'))

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
    message_text = f'Monthly Video Stream Report\n'
    msg.attach(MIMEText(message_text, 'plain')) 
    #f'Click the following link to reset your password: {reset_link}', 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)


if __name__ == '__main__':
    send_download_link(to='gatto@nanowar.it', code='dummy-test-666')

