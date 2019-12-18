from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from bloodbank.models import Gallery,Feedback, Hospitals,User, Campadd
from flask_login import current_user


class Register(FlaskForm):
    name=TextField('Name',validators=[DataRequired(), Length(min=1, max=400)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    age = StringField('Age',validators=[DataRequired(), Length(min=1, max=400)])
    bloodgroup= StringField('Blood Group',validators=[DataRequired(), Length(min=1, max=400)])
    address = StringField('Address',validators=[DataRequired(), Length(min=1, max=400)])
    city = StringField('City',validators=[DataRequired(), Length(min=1, max=400)])
    state= StringField('State',validators=[DataRequired(), Length(min=1, max=400)])
    mobile = StringField('Mobile', validators=[DataRequired(), Length(min=1, max=400)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')
            flash('error')


class Addhospitals(FlaskForm):
    name= TextField('Hospital Name', validators=[DataRequired(), Length(min=1, max=400)])
    place= StringField('Place', validators=[DataRequired(), Length(min=1, max=400)])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=1, max=400)])
    mobile = StringField('Mobile', validators=[DataRequired(), Length(min=1, max=400)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    agroup = StringField('Available BloodGroup', validators=[DataRequired(), Length(min=1, max=400)])
    rgroup = StringField('required BloodGroup', validators=[DataRequired(), Length(min=1, max=400)])
    pic = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Save')

class Addimage(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=40)])
    pic = FileField('Upload Picture', validators=[DataRequired(),FileAllowed(['jpg', 'png','jpeg'])])
    submit = SubmitField('Save')


class Feedback(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=5, max=40)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=1, max=400)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=40)])
    message =StringField('Message', validators=[DataRequired(), Length(min=5, max=40)])
    submit = SubmitField('Sent Message')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login') 


class Accountform(FlaskForm):
    name = StringField('Name',
                           validators=[ Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[Email()])
    age= StringField('Age',
                           validators=[ Length(min=2, max=20)])
    address= StringField('Address',
                           validators=[ Length(min=2, max=20)])
    city= StringField('City',
                           validators=[ Length(min=2, max=20)])
    state= StringField('State',
                           validators=[ Length(min=2, max=20)])
    mobile = StringField('Mobile',
                           validators=[ Length(min=2, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


class Accountform1(FlaskForm):
    name = StringField('Name',
                           validators=[ Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')



class Changepassword(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[ EqualTo('password')])
    submit = SubmitField('Reset Password')

class Requestresetform(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')



class Camp(FlaskForm):
    date = StringField('Date',render_kw={"placeholder": "dd-mm-yyyy"})
                
    desc = StringField('Description',validators=[ Length(min=2, max=20)])
    place= StringField('Place',
                           validators=[ Length(min=2, max=20)])
    mobile = StringField('Mobile',
                           validators=[ Length(min=2, max=20)])
    pic = FileField('Upload Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')