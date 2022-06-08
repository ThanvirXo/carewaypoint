from turtle import title
from flask import render_template,url_for,flash,redirect, request
from careway.forms import RegistrationForm,LoginForm, RequestResetForm, ResetPasswordForm,UserInterestForm
from careway import app,db,bcrypt,mail
from careway.models import User
from flask_login import login_user, current_user,logout_user
from flask_mail import Message
from careway import model
from . import target_classnames
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from collections import OrderedDict
#Aqua Routes


@app.before_first_request
def startup():
  global data, model, target_classnames
  df = pd.read_csv('careway\CWPP.csv')
  target = df.target
  df.drop('target_classnames', axis=1, inplace=True)
  df.drop('target', axis=1, inplace=True)
  data = df.to_numpy()
  target_classnames = ['Data Scientist', 'Full Stack Developer', 'Big Data Engineer', 'Database Administrator', 'Cloud Architect',
                       'Cloud Services Developer ', 'Network Architect', 'Data Quality Manager', 'Machine Learning', 'Business Analyst']
  model = MultinomialNB(alpha=1)
  model.fit(data, target)
  
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash( 'Your account has been created! Now you are able to login','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)



@app.route("/login",methods=['GET','POST'] )
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))    
        flash('Login Unsuccessful.Please check your Credentials!', 'danger')
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))




def send_reset_email(user):
    token=user.get_reset_token()
    msg= Message('Password Reset Request',sender='carewaypoint@gmail.com',recipients=[user.email])
    msg.body= f'''To reset your password,visit the following link:
{url_for('reset_token', token=token  , _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.    
'''
    mail.send(msg)


    


@app.route("/reset_password",methods=['GET','POST'] )
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with an instruction to reset your password.Please check your spam inbox.','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html',title='Reset Password',form=form)

@app.route("/reset_password/<token>",methods=['GET','POST'] )
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user=User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token.','warning')
        return redirect(url_for('reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash( 'Your Password has been Updated! Now you are able to login','success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password',form=form)



@app.route("/user_form",methods=['POST','GET'])
def user_form():
    form=UserInterestForm()
    
    return render_template('form.html',title='Prediction',form=form)


@app.route("/suggest", methods=["GET","POST"])
def suggest():
    form = UserInterestForm()
    ar=[0 for i in range(11)]
    d = {"B.E Computer Science": 0, "B.E Information Technology": 3, "M.E Computer Science": 6, "B.E Electrical and Electronics engineering": 1, "B.E Electrical and Communication engineering": 2, "M.Sc Computer science":9,
    "B.Sc Computer Science":4,"Bachelor Computer Application":5,"M.E B.E Electrical and Electronics engineering":7,"M.E Electrical and Communication engineering":8,"M.Tech/M.E Information Technology":10}
    print(ar)
    print("IN FORM")
    und = request.form['und']
    pnd = request.form['pnd']
    if und!="None" and pnd!="None":
        degrees=[und,pnd]
        for i in degrees:
            ar[d[i]]=1
    

    verdict=predict(ar)
    levels=predictLevels(ar)
    print(levels)
    finalLevels = sorted(levels.items(), key=lambda x: x[1], reverse=True)
    return render_template('form.html', title='Prediction', form=form, verdict=verdict['prediction'], levels=finalLevels)


def predict(array):
    print("TARGET", target_classnames)
    print("MODEL",model)
#   if request.method == 'POST':
#     request_data = request.get_json()
#     array = [request_data['data']]
    narray=[array]
    predict = model.predict(narray)
    print("PREDICT", predict)
    predict_levels = model.predict_proba(narray)
    print(predict_levels[0])
    # The above code is for the levels which you need to order
    return {'prediction': target_classnames[predict[0]]}

def predictLevels(array):
    narray=[array]
    predict_levels = model.predict_proba(narray)
    predict_levels_list = predict_levels[0].tolist()
    res = {}
    for key in target_classnames:
        for value in predict_levels_list:
            res[key] = value
            predict_levels_list.remove(value)
            break
    return(res)
