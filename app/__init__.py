from flask import Flask, render_template, request, abort, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, UserServer
import re
from sqlalchemy import func
import DataFormater.RandomPhotoPickerOneToFour as rpp
from functools import wraps

# inicjalizacja aplikacji
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "current_user" not in session:
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

def create_account(uname, pwd, birth_year=None, residency=None, sex=None, account_type=None):
    pwd_hash = generate_password_hash(pwd)
    if account_type == 'user':
        print("siema")
        new_user_data = User(birthYear = birth_year, sex=sex, placeOfResidence=residency) #personal data of the user
        db.session.add(new_user_data)
        fresh_user = db.session.query(func.max(User.userId)).scalar()
        new_user_server = UserServer(username=uname, password=pwd_hash, type=account_type, userId=fresh_user) #login data for the user
        db.session.add(new_user_server)
    else:
        new_user_server = UserServer(username=uname, password=pwd_hash, type=account_type) #login data for the user
        db.session.add(new_user_server)

    db.session.commit() #adding user into login db and data db

def map_residency_vals(val):
    residency_mapping = {
        1: "village",
        2: "city <20k",
        3: "city 20k-100k",
        4: "city >100k"
    }
    return residency_mapping.get(val, "unknown")

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

@app.route("/who-are-you", methods=['GET', 'POST'])
def who_are_you():
    if request.method == 'POST':
        val = str(request.form.get('role'))
        if val == 'user' or val == 'scientist':
            session['user_type'] = val
            return redirect(url_for('register'))
    return render_template('choose.html')
        
@app.route("/register", methods=['GET', 'POST'])
def register():
    #if request.method == 'GET':
    if request.method == 'POST':
        u = str(request.form.get('username_signup'))
        p = str(request.form.get('password_signup'))     
        pc = str(request.form.get('confirm_password'))

        
        print(u, p, pc)
        account_type = session['user_type']
        if account_type == 'user': #not 'scientist'
            birth_year = int(str(request.form.get('birth_year'))[:4])  # parsing birth year from birth date
            sex = str(request.form.get('gender'))   

            residency = int(str(request.form.get('residence')))        # parsing residency based on html form
            residency = map_residency_vals(residency)

        #u, p, pc = '', 'zaq1@WSX', 'zaq1@WSX'

        print(u, p, pc)

        # validation starts here
        if len(u) == 0:                                               # null username
            flash(message='Username cannot be empty.', category=None)
            return redirect(url_for('register'))
        if p != pc:                                                   # incorrect pwd == pwdconfirm
            flash(message='Passwords have to match.', category=None)
            return redirect(url_for('register'))
        
        exist_check = UserServer.query.filter_by(username=u).first()  # does the account already exist?
        if exist_check:
            flash(message='Account with this username already exists.', category=None)
            return redirect(url_for('register'))          
        
                                                                      # does the password match the regex?
        if not re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$", p):
            # min. 8 chars, >=1 upper case English letter, >=1 lower case English letter, 
            # >=1 number and >=1 special character
            flash(message='Password must include: min. 8 characters: 1 uppercase, 1 lowercase, 1 digit, 1 special.', category=None)
            return redirect(url_for('register'))
        
        if account_type == 'user':
            create_account(u, p, birth_year, sex, residency, account_type)              # allow creation
            return redirect(url_for('home'))  
        elif account_type == 'scientist':
            create_account(u, p, account_type='scientist')              # allow creation
            return redirect(url_for('home'))                           
    return render_template("register.html")                                                        # unknown error

@login_required
@app.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        next_form = str(request.form.get('form_value'))
        redirect(url_for('test_' + next_form))
    return render_template('home.html')

@login_required
@app.route("/quiz1", methods=['GET', 'POST'])
def quiz_form1():
    random_tuple = rpp.choose_correct_emotion()
    point_dict = {}
    point_dict[str(random_tuple[0])] = 1

    for i in range(0, len(random_tuple[1])):
        point_dict[str(random_tuple[1][i])] = 0
    
    for k, v in point_dict.items():  #debug
        print(k, v)         
    return render_template("quiz1.html")

@login_required
@app.route("/results")
def results():
    pass

@login_required
@app.route("/account")
def account():
    pass

if __name__ == "__main__":
    app.run(debug=True)