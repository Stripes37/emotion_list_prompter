from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'instance', 'emotions.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

scheduler = BackgroundScheduler()
scheduler.start()

class Emotion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    main_category = db.Column(db.String(50), nullable=False)
    sub_category = db.Column(db.String(50), nullable=False)
    trigger = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Emotion {self.main_category} - {self.sub_category}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        main_category = request.form['main_category']
        sub_category = request.form['sub_category']
        trigger = request.form['trigger']
        description = request.form['description']
        rating = request.form['rating']
        new_entry = Emotion(main_category=main_category, sub_category=sub_category, trigger=trigger, description=description, rating=rating)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/api/emotions', methods=['POST'])
def add_emotion():
    data = request.get_json()
    main_category = data.get('main_category')
    sub_category = data.get('sub_category')
    trigger = data.get('trigger')
    description = data.get('description')
    rating = data.get('rating')
    new_entry = Emotion(main_category=main_category, sub_category=sub_category, trigger=trigger, description=description, rating=rating)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'message': 'Emotion added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
