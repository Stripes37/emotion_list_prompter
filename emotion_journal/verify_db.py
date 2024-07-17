from app import app, db

with app.app_context():
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    if 'emotion' in tables:
        print("The Emotion table exists in the database.")
    else:
        print("The Emotion table does not exist in the database.")
