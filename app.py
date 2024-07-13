from flask import Flask, jsonify, request
from celery import Celery
import smtplib
from email.mime.text import MIMEText
import logging
from datetime import datetime
import os


app = Flask(__name__)

# Configur ecelery
celery = Celery(app.name, broker='pyamqp://guest@localhost//')

# env details
SENDER_EMAIL = 'rubyroe17@gmail.com'
SENDER_PASSWORD = 'xlhzamodiaoxkofg'

logger = logging.getLogger(__name__)
LOG_FILE_PATH = '/var/log/messaging_system.log' #Ensure file exsits with necessary permissions

@celery.task
def send_email(receiver):
    sender = SENDER_EMAIL
    password = SENDER_PASSWORD
    msg = MIMEText('HNG TASK 3: This is a test email sent from the messaging system using Python and Celery.')
    msg['Subject'] = 'Testing 1...2...3'
    msg['From'] = sender
    msg['To'] = receiver
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, receiver, msg.as_string())
        logging.info(f"Email sent to {receiver} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
   
@celery.task
def log_current_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Talktome request received at {current_time}")

@app.route('/')
def handle_request():
    
    if 'sendmail' in request.args:
        recipient = request.args.get('sendmail')
        send_email.delay(recipient)
        return f"Email task created for sending to {recipient}"
    
    elif 'talktome' in request.args:
        with open(LOG_FILE_PATH, 'a') as log_file:
            log_message = f"{datetime.now()} - Talk to me endpoint accessed"
            log_file.write(log_message + '\n')
            logger.info(log_message)
        return "Talk to me parameter logged"
    else:
        return "Hello, This works fine. Kindly provide your parameter in th url"
    
@app.route('/logs')
def get_logs():
    if not os.path.exists(LOG_FILE_PATH):
        return jsonify({"error": "Log file does not exist"}), 404

    with open(LOG_FILE_PATH, 'r') as log_file:
        logs = log_file.readlines()

    return jsonify({"logs": logs})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0, port=8000')
