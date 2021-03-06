from flask import Flask, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm,CSRFProtect
from flask_mail import Mail



app=Flask(__name__)

app.config['SECRET_KEY'] = '8ea2a86e42689205dde0ba81f31138b6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloodbank.db'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'arjun.fabstudioz@gmail.com'
app.config['MAIL_PASSWORD'] = 'arjun1234'
app.config['MAIL_DEFAULT_SENDER'] = 'arjun.fabstudioz@gmail.com'
mail = Mail(app)



from bloodbank import routes