from app import app, db
from models import Emotion

with app.app_context():
    # Query the database to check if the Emotion table exists
    tables = db.engine.table_names()
    if 'emotion' in tables:
        print("The Emotion table exists in the database.")
    else:
        print("The Emotion table does not exist in the database.")
