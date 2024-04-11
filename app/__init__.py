from flask import Flask, render_template, request, abort, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, UserServer
import excel_fetch
import re

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
    return "Hi"

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if request.form.get('username') in UserServer.query.all(): #is there an account with this username?
            return 'registration failed - account already exists'
        if re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$", request.form.get('password')):
            # Minimum eight characters, at least one upper case English letter, one lower case English letter, one number and one special character
            # does the password match the regex?
            return 'registration successful'
            # CODE HERE TO INPUT DATA INTO DATABASE
        else:
            return 'registration failed - Password must match regex'
    return "?"

@app.route("/results")
def results():
    pass

@app.route("/account")
def account():
    pass

if __name__ == "__main__":
    app.run(debug=True)