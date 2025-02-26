import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import xxyears.video as vid
import pandas as pd
from datetime import datetime, timedelta


def create_backup(file_path='static/codes_used.csv'):
    """
    Creates a backup of the specified CSV file with a .bkp extension.

    :param file_path: Path to the original CSV file
    """
    try:
        backup_path = f"{file_path}.bkp"
        with open(file_path, 'r') as original_file:
            with open(backup_path, 'w') as backup_file:
                backup_file.write(original_file.read())
        print(f"Backup created successfully: {backup_path}")
    except Exception as e:
        print(f"Error creating backup: {e}")


def generate_codes_report(csv_path='static/codes_used.csv'):
    """
    Generate a comprehensive report of codes from the CSV file.

    :param csv_path: Path to the CSV file containing code information
    :return: Dictionary with code statistics
    """
    try:
        # Read the CSV file

        try:
            custom_header = ['mail', 'code', 'sale_date', 'status']
            df = pd.read_csv(csv_path, header=None, names=custom_header)
            print("CSV content read successfully: \n", df.head())
        except Exception as e:
            raise RuntimeError(f"Failed to read the CSV file at {csv_path}: {e}")

        # Current date and last week's date
        today = datetime.now().date()
        last_week = today - timedelta(days=7)

        # Total codes
        total_codes = len(df)
        print("Total codes:", total_codes)

        # Redeemed codes
        redeemed_codes = df[df['status'] == 'REDEEMED']
        total_redeemed = len(redeemed_codes)
        print("Redeemed codes data:\n", redeemed_codes)
        print("Total redeemed codes:", total_redeemed)

        # Sold codes
        sold_codes = df[df['status'] == 'SOLD']
        total_sold = len(sold_codes)
        print("Sold codes data:\n", sold_codes)
        print("Total sold codes:", total_sold)

        # Codes sold last week
        last_week_sold = sold_codes[pd.to_datetime(sold_codes['sale_date']).dt.date.between(last_week, today)]
        total_last_week_sold = len(last_week_sold)
        print("Codes sold last week data:\n", last_week_sold)
        print("Total codes sold last week:", total_last_week_sold)

        # Codes sold today
        today_sold = sold_codes[pd.to_datetime(sold_codes['sale_date']).dt.date == today]
        total_today_sold = len(today_sold)
        print("Codes sold today data:\n", today_sold)
        print("Total codes sold today:", total_today_sold)

        link_part1, link_part2, link_part3 = vid.return_video_urls()


        # Compile report
        report = f"""
Video Codes Report - {today}
----------------------------

Total Codes: {total_codes}
Total Redeemed Codes: {total_redeemed}
Total Sold Codes: {total_sold}

Codes Sold Last Week: {total_last_week_sold}
Codes Sold Today: {total_today_sold}
----------------------------

Latest video links:
----------------------------
 <br>
 <a href={link_part1}>PART 1</a>
 <br>
 <a href={link_part2}>PART 2</a>
 <br>
 <a href={link_part3}>PART 3</a>
 <br>

"""
        return report

    except Exception as e:
        return f"Error generating report: {str(e)}"


def send_codes_report(mail_to='gatto@nanowar.it',
                      subject='XX Years of Steel - Codes Report',
                      csv_path='xxyears/static/codes_used.csv'):
    """
    Generate and send codes report via email.

    :param mail_to: Recipient email address
    :param subject: Email subject
    :param csv_path: Path to the CSV file
    """
    # Generate report
    report = generate_codes_report(csv_path)
    print(report)

    # Send email with report (using existing email infrastructure)
    smtp_server = 'smtp.xxyearsofsteel.com'
    smtp_port = 587
    smtp_config_file = 'json/.smtp_credentials.json'

    if smtp_config_file:
        try:
            import json
            with open(smtp_config_file, 'r') as f:
                smtp_config = json.load(f)
            smtp_username = smtp_config.get('SMTP_USERNAME_INFO')
            smtp_password = smtp_config.get('SMTP_PASSWORD')
        except Exception as e:
            raise RuntimeError(f"Failed to read SMTP configuration file: {e}")
    else:
        smtp_username = os.environ.get('SMTP_USERNAME_INFO')
        smtp_password = os.environ.get('SMTP_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = 'info@xxyearsofsteel.com'
    msg['To'] = mail_to
    msg['Subject'] = subject

    msg.attach(MIMEText(report, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

def send_download_link(to : str, code : str):

    # Send email with album code
    smtp_server = 'smtp.xxyearsofsteel.com'
    smtp_port = 587
    smtp_config_file = 'json/.smtp_credentials.json'

    if smtp_config_file:
        try:
            import json
            with open(smtp_config_file, 'r') as f:
                smtp_config = json.load(f)
            smtp_username = smtp_config.get('SMTP_USERNAME_INFO')
            smtp_password = smtp_config.get('SMTP_PASSWORD')
        except Exception as e:
            raise RuntimeError(f"Failed to read SMTP configuration file: {e}")
    else:
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
    smtp_config_file = 'json/.smtp_credentials.json'

    if smtp_config_file:
        try:
            import json
            with open(smtp_config_file, 'r') as f:
                smtp_config = json.load(f)
            smtp_username = smtp_config.get('SMTP_USERNAME_INFO')
            smtp_password = smtp_config.get('SMTP_PASSWORD')
        except Exception as e:
            raise RuntimeError(f"Failed to read SMTP configuration file: {e}")
    else:
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
