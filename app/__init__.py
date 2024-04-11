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

def create_account(uname, pwd):
    pwd_hash = generate_password_hash(pwd)
    new_user = UserServer(username=uname, password=pwd_hash)
    db.session.add(new_user)
    db.session.commit()


db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/", methods=['GET', 'POST'])
def index():
    #if request.method == 'POST':
     #   uname = request.form.get('username')
      #  pwd = request.form.get('password')
       # if uname in UserServer.query.all():
            
        return render_template('choose.html')

@app.route("/login", methods=['GET', 'POST'])
def who_are_you():
    pass

@app.route("/register", methods=['GET', 'POST'])
def register():
    u, p = "abcdefgasdfhasd", "zaqWSX"
    if request.method == 'GET':
        exist_check = UserServer.query.filter_by(username=u).first()
        if exist_check:
            return 'registration failed - account already exists'            
        if re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$", p):
            # Minimum eight characters, at least one upper case English letter, one lower case English letter, one number and one special character
            # does the password match the regex?
            create_account(u, p)
            return 'registration successful'
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