from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emotions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Twilio credentials (replace with your actual credentials)
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'
USER_PHONE_NUMBER = 'your_phone_number'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_notification():
    message = client.messages.create(
        body="How are you feeling right now? Reply with your emotion and why.",
        from_=TWILIO_PHONE_NUMBER,
        to=USER_PHONE_NUMBER
    )
    print(message.sid)

scheduler = BackgroundScheduler()
scheduler.add_job(send_notification, 'interval', hours=2)  # Change as needed
scheduler.start()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        emotion = request.form['emotion']
        reason = request.form['reason']
        new_entry = Emotion(emotion=emotion, reason=reason)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html')

if __name__ == '__main__':
    from models import Emotion  # Import here to avoid circular import
    app.run(debug=True)
