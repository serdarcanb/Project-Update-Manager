from flask import Flask, request
from app.backend import main_backend
from dotenv import load_dotenv
from notification.discord import notification_send_message
import os

app = Flask(__name__)

load_dotenv()
SAFE_TOKEN = os.getenv('SAFE_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

@app.route('/update-project', methods=['POST'])
def update_project():
    if request.headers.get('Authorization') == f'Bearer {SAFE_TOKEN}':
        main_backend()
        return "Successfully", 200
    else:
        notification_send_message("401  /update-project",CHANNEL_ID)
        return "Authorization failed.", 401

@app.route('/health')
def health_check():
    return "Yes Sir!", 200

if __name__ == '__main__':
    app.run(host=os.getenv('WEB_APP_HOST'), port=os.getenv('WEB_APP_PORT'))
