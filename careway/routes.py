from flask import render_template,url_for,flash,redirect, request
from careway.forms import RegistrationForm,LoginForm, RequestResetForm, ResetPasswordForm
from careway import app,db,bcrypt,mail
from careway.models import User
from flask_login import login_user, current_user,logout_user
from flask_mail import Message

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
