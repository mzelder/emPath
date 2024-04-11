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
    if request.method == 'POST':
        uname, pwd = str(request.form.get('username')), str(request.form.get('password'))
        user = UserServer.query.filter_by(username=uname).first()
        if user and check_password_hash(user.password, pwd):
            session["current_user"] = uname
            return render_template('home.html')
        flash(message="Invalid username or password.", category=None)       
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    #if request.method == 'GET':
    if request.method == 'POST':
        u, p = str(request.form.get('username')), str(request.form.get('password'))
        #u, p = "qwerty", "zaq1@WSX"
        exist_check = UserServer.query.filter_by(username=u).first()  # does the account already exist?
        if exist_check:
            return 'registration failed - account already exists'            
        if re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$", p):
            # Minimum eight characters, at least one upper case English letter, one lower case English letter, one number and one special character
            # does the password match the regex?
            create_account(u, p)
            return render_template('home.html')
        else:
            return 'registration failed - Password must match regex'
    return "?"


@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/results")
def results():
    pass

@app.route("/account")
def account():
    pass

if __name__ == "__main__":
    app.run(debug=True)