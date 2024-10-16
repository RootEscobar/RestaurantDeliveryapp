from flask import Flask
from authy.api import AuthyApiClient
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)          #SQLALCHEMY_DATABASE_URI = 'mssql://DARB\SQLEXPRESS:password@localhost/db_rest'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/alega/Documents/GitHub/RestaurantDeliveryapp/restaurant/restaurant/tables.db'
app.config['SECRET_KEY'] = '325766a2074f2402bf2e19eb7cc35430'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page" #to redirect user to login page if login required

#OTP API
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']
api = AuthyApiClient(app.config['AUTHY_API_KEY'])

from restaurant import routes 
