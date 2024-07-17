from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emotions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

scheduler = BackgroundScheduler()
scheduler.start()

class Emotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emotion = db.Column(db.String(50), nullable=False)
    reason = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Emotion {self.emotion}>'

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

@app.route('/api/emotions', methods=['POST'])
def add_emotion():
    data = request.get_json()
    emotion = data.get('emotion')
    reason = data.get('reason')
    new_entry = Emotion(emotion=emotion, reason=reason)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'message': 'Emotion added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
