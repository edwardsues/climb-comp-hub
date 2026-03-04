from main import app, db


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()  # Deletes all tables
        db.create_all()  # Creates them fresh with new schema
        print("Tables recreated!")