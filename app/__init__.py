from flask import Flask, render_template, request, abort, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

# inicjalizacja aplikacji
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return "TEST2"

if __name__ == "__main__":
    app.run(debug=True)