from flask import Flask, render_template, request, abort, session, redirect, url_for, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, UserServer, Training_Session_Result
import re
import os
import pandas as pd
import DataFormater.ExcelFetch as EF
import DataFormater.DataFormater
import DataFormater.JsonChecker
import DataFormater.PhotoDataChecker
import json
from sqlalchemy import func
import DataFormater.RandomPhotoPickerOneToFour as q1handle
import DataFormater.Random4Photos1Emotion as q2handle
import DataFormater.OneEmotionTwoPhotos as q3handle
import DataFormater.OnePhotoOneIntensity as q4handle
from functools import wraps
import random as r
import math as m
from flask_sqlalchemy import SQLAlchemy

# inicjalizacja aplikacji
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/signout")
def signout():
    session.clear()
    return redirect(url_for("index"))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "current_user" not in session:
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

def create_account(uname, pwd, birth_year=None, residency=None, sex=None, account_type=None):
    pwd_hash = generate_password_hash(pwd)
    uname_hash = generate_password_hash(uname)
    if account_type == 'user':
        new_user_data = User(birthYear = birth_year, sex=sex, placeOfResidence=residency) #personal data of the user
        db.session.add(new_user_data)
        fresh_user = db.session.query(func.max(User.userId)).scalar()
        new_user_server = UserServer(username=uname, password=pwd_hash, type=account_type, userId=fresh_user) #login data for the user
        db.session.add(new_user_server)
    else:
        new_user_server = UserServer(username=uname_hash, password=pwd_hash, type=account_type) #login data for the user
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

@app.route("/", methods=['GET', 'POST'])
def index():
    if session.get('current_user'):
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        uname, pwd = str(request.form.get('username')), str(request.form.get('password'))
        user = UserServer.query.filter_by(username=uname).first()
        if user and check_password_hash(user.password, pwd):
            session["current_user"] = uname
            session["user_type"] = user.type
            return render_template('home.html')
        flash(message=f"Invalid username or password.", category="danger")       
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
            flash(message='Username cannot be empty.', category="danger")
            return redirect(url_for('register'))
        if p != pc:                                                   # incorrect pwd == pwdconfirm
            flash(message='Passwords have to match.', category="danger")
            return redirect(url_for('register'))
        
        exist_check = UserServer.query.filter_by(username=u).first()  # does the account already exist?
        if exist_check:
            flash(message='Account with this username already exists.', category="danger")
            return redirect(url_for('register'))          
        
                                                                      # does the password match the regex?
        if not re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$", p):
            # min. 8 chars, >=1 upper case English letter, >=1 lower case English letter, 
            # >=1 number and >=1 special character
            flash(message='Password must include: min. 8 characters: 1 uppercase, 1 lowercase, 1 digit, 1 special.', category="danger")
            return redirect(url_for('register'))
        
        session["current_user"] = u
        if account_type == 'user':
            create_account(u, p, birth_year, sex, residency, account_type)              # allow creation
            return redirect(url_for('home'))  
        elif account_type == 'scientist':
            create_account(u, p, account_type='scientist')                              # allow creation
            return redirect(url_for('home'))                           
    return render_template("register.html")                                             # unknown error


@app.route("/home", methods=['GET', 'POST'])
#@login_required
def home():
    if request.method == 'POST':
        next_form = str(request.form.get('form_value'))
        return redirect(url_for(next_form))
    return render_template('home.html')


@app.route("/quiz1", methods=['POST', "GET"])
#@login_required
def quiz1():
    # if request.method == "GET":
    #     return redirect(url_for('home'))
    
    if 'q1_time_start' not in session:
        session['q1_time_start'] = db.session.query(func.now()).scalar().astimezone()

    if 'q1_question_sequence' not in session:
        session['q1_question_sequence'] = []

    if 'q1_question_count' not in session:
        session['q1_question_count'] = 0

    if request.method == 'POST':
        ans = str(request.form.get('answer'))  # Convert answer to integer directly
        correct_answer = session.get('q1_correct_answer')
        session['q1_question_sequence'].append((session['q1_question_count'], ans, correct_answer))
        session['q1_question_count'] += 1
        return redirect(url_for('quiz1'))
    
    if session['q1_question_count'] < 20:
        random_tuple = q1handle.choose_correct_emotion()
        session['q1_correct_answer'] = random_tuple[0]
        point_dict = {str(random_tuple[0]): 1}

        for item in random_tuple[1]:
            point_dict[str(item)] = 0

        emotions = list(point_dict.keys())
        r.shuffle(emotions)

        print(emotions, random_tuple[2], random_tuple[0])

        return render_template('quiz1.html', i=session['q1_question_count'], emotions=emotions, img_src=random_tuple[2])
    else:
        session['quiz_redirect'] = 1
        return redirect(url_for('results'))
    
    
@app.route('/download-db')
def download_db():
    directory = os.path.join(app.instance_path)  # Path to your instance folder
    print(directory)
    filename = 'db.sqlite3'
    return send_from_directory(directory, filename, as_attachment=True)
    


@app.route("/quiz2", methods=['GET', 'POST'])
#@login_required
def quiz2():
    #if request.method == "GET":
    #    return redirect(url_for('home'))
    
    if 'q2_time_start' not in session:
        session['q2_time_start'] = db.session.query(func.now()).scalar().astimezone()

    if 'q2_question_sequence' not in session:
        session['q2_question_sequence'] = []

    if 'q2_question_count' not in session:
        session['q2_question_count'] = 0

    if request.method == 'POST':
        ans = str(request.form.get('answer'))  # Convert answer to integer directly
        correct_answer = session.get('q2_correct_answer')
        session['q2_question_sequence'].append((session['q2_question_count'], ans, correct_answer))
        session['q2_question_count'] += 1
        return redirect(url_for('quiz2'))
    
    if session['q2_question_count'] < 20:
        random_tuple = q2handle.generate_output()
        session['q2_correct_answer'] = random_tuple[0]
        point_dict = {str(random_tuple[0]): 1}

        for item in random_tuple[1]:
            point_dict[str(item)] = 0

        photos = list(point_dict.keys())
        r.shuffle(photos)

       #print(photos, random_tuple[2], random_tuple[0])

        return render_template('quiz2.html', i=session['q2_question_count'], photos=photos, emotion=random_tuple[2])
    else:
        session['quiz_redirect'] = 2
        return redirect(url_for('results')) 


@app.route("/quiz3", methods=['GET', 'POST'])
@login_required
def quiz3():
    #if request.method == "GET":
    #    return redirect(url_for('home'))
    
    if 'q3_time_start' not in session:
        session['q3_time_start'] = db.session.query(func.now()).scalar().astimezone()

    if 'q3_question_sequence' not in session:
        session['q3_question_sequence'] = []

    if 'q3_question_count' not in session:
        session['q3_question_count'] = 0

    if request.method == 'POST':
        ans = str(request.form.get('answer'))  # Convert answer to integer directly
        correct_answer = session.get('q3_correct_answer')
        session['q3_question_sequence'].append((session['q3_question_count'], ans, correct_answer))
        session['q3_question_count'] += 1
        return redirect(url_for('quiz3'))
    
    if session['q3_question_count'] < 10:
        random_tuple = q3handle.get_output()
        session['q3_correct_answer'] = random_tuple[0]
        point_dict = {str(random_tuple[0]): 1}

        for item in random_tuple[1]:
            point_dict[str(item)] = 0

        photos = list(random_tuple)
        r.shuffle(photos)



        return render_template('quiz3.html', i=session['q3_question_count'], photos=photos)
    else:
        session['quiz_redirect'] = 3
        return redirect(url_for('results'))

@app.route("/quiz4", methods=['GET', 'POST'])
@login_required
def quiz4():
    #if request.method == "GET":
    #    return redirect(url_for('home'))
    # print(session['q4_question_count'])

    if 'q4_time_start' not in session:
        session['q4_time_start'] = db.session.query(func.now()).scalar().astimezone()

    if 'q4_question_sequence' not in session:
        session['q4_question_sequence'] = []

    if 'q4_question_count' not in session:
        session['q4_question_count'] = 0

    if request.method == 'POST':
        ans = float(request.form.get('range-q4'))  # Convert answer to integer directly
        correct_answer = session.get('q4_correct_answer')
        print(correct_answer)
        session['q4_question_sequence'].append((session['q4_question_count'], ans, correct_answer))
        session['q4_question_count'] += 1
        return redirect(url_for('quiz4'))
    
    if session['q4_question_count'] < 15:
        random_tuple = q4handle.get_output()
        print(random_tuple)
        session['q4_correct_answer'] = random_tuple[1]
        #print(random_tuple[0], random_tuple[1])
        return render_template('quiz4.html', i=session['q4_question_count'], photo=random_tuple[0])
    else:
        session['quiz_redirect'] = 4
        return redirect(url_for('results'))

@app.route("/results")
@login_required
def results():
    d = {}
    for el in session["q" + str(session['quiz_redirect']) + "_question_sequence"]:
        if session['quiz_redirect'] < 4:
            d[el[0] + 1] = el[1] == el[2]
        else:
            threshold = 0.1
            print(el[1], el[2], "xddddd")
            d[el[0] + 1] = abs(el[1] - el[2]) <= threshold
    score = sum(d.values())
    perc = m.ceil(sum(d.values()) / len(d.items()) * 100)

    curr_user = UserServer.query.filter_by(username=session["current_user"]).first()
    last_session = Training_Session_Result.query.filter_by(userId=curr_user.userId).first()
    if last_session:
        session_type = 'training'
    else:
        session_type = 'diagnosis'
    
    if session['quiz_redirect'] == 1:
        t_type = 'Choose Emotion'
    if session['quiz_redirect'] == 2:
        t_type = 'Choose Person'
    if session['quiz_redirect'] == 3:
        t_type = 'Intensity Comparison Training'
    if session['quiz_redirect'] == 4:
        t_type = 'Intensity Estimation Training'

    new_session = Training_Session_Result(userId=curr_user.userId, startedAt=session['q' + str(session['quiz_redirect']) + '_time_start'],\
                                           endedAt=db.session.query(func.now()).scalar(), \
                                            type=session_type,\
                                            score=score, total_score = len(d.items()), test_type=t_type)
    
    db.session.add(new_session)
    db.session.commit()

    del session['q' + str(session['quiz_redirect']) + '_time_start']
    del session['q' + str(session['quiz_redirect']) + '_question_sequence']
    del session['q' + str(session['quiz_redirect']) + '_question_count']
    del session['q' + str(session['quiz_redirect']) + '_correct_answer']
    return render_template("results.html", questions=d, score=score, perc=perc, total_questions=len(d.items()))


@app.route("/profile")
@login_required
def profile():
    curr_user = UserServer.query.filter_by(username=session["current_user"]).first()
    training_sessions = Training_Session_Result.query.filter_by(userId=curr_user.id).all()
    params = []
    for i in range(len(training_sessions)):
        params.append([i + 1, training_sessions[i].endedAt, training_sessions[i].score, training_sessions[i].total_score,\
                       m.ceil(training_sessions[i].score/training_sessions[i].total_score*100), training_sessions[i].test_type])
    return render_template("profile.html", params=params)

if __name__ == "__main__":
    app.run(debug=False)