import os
import smtplib

SMTP_SERVER = "smtp.nanowar.it"
PORT = 587
EMAIL = os.environ.get("NANO_MAIL")
PASSWORD = os.environ.get("NANO_PASS")
SITE_URL = 'https://downloadportal.onrender.com/auth/register'

def sendmail(mail_to='gatto@nanowar.it', subject='Your XX Years Of Steel Code', code='this-is-dummy-666'):
    to = mail_to
    sender = EMAIL 
    smtpserver = smtplib.SMTP(SMTP_SERVER,PORT)
    user = EMAIL
    password = PASSWORD 
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(user, password)
    header = 'To:' + to + '\n' + 'From: ' + sender + '\n' + 'Subject:' + subject + '\n'
    message = f'{header}\n Thanks for your purchase!\n\n You can now register on: \n {SITE_URL} \n\n using the code: \n {code} \n\n Enjoy the show!'
    smtpserver.sendmail(sender, to, message)
    smtpserver.close()


if __name__ == '__main__':
    sendmail()

