import os
from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_mail import Mail
from careway.handlers import errors


#Aquaman requirements
from operator import mod
from werkzeug.utils import secure_filename
from flask_cors import CORS
import logging
import _tkinter
import pandas as pd
import numpy as np
from sklearn.naive_bayes import MultinomialNB
import json

app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY']='03444959c853297b31284bea27285015'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

data = None
model = None
target_classnames = None


# @app.before_first_request
# def startup():
#   global data, model, target_classnames
#   df = pd.read_csv('D:\Projects\carewaypoint\carewaypoint\careway\CWPP.csv')
#   target = df.target
#   df.drop('target_classnames', axis=1, inplace=True)
#   df.drop('target', axis=1, inplace=True)
#   data = df.to_numpy()
#   target_classnames = ['Data Scientist', 'Full Stack Developer', 'Big Data Engineer', 'Database Administrator', 'Cloud Architect',
#                        'Cloud Services Developer ', 'Network Architect', 'Data Quality Manager', 'Machine Learning', 'Business Analyst']
#   model = MultinomialNB(alpha=1)
#   model.fit(data, target)


# @app.route("/predict", methods=['POST', 'GET'])
# def predict():
#   if request.method == 'POST':
#     request_data = request.get_json()
#     array = [request_data['data']]
#     predict = model.predict(array)
#     predict_levels = model.predict_proba(array)
#     print(predict_levels[0])
#     # The above code is for the levels which you need to order
#     return {'prediction': target_classnames[predict[0]]}


db = SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'
app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('EMAIL_NAME')
app.config['MAIL_PASSWORD']=os.environ.get('EMAIL_WORD')
mail=Mail(app)
app.register_blueprint(errors)

from careway import routes
