import os
from flask import Flask, flash, session
from flask import render_template, flash, redirect, request, abort, url_for
from bloodbank import app,db, bcrypt,  mail
from bloodbank.forms import Addimage,Addhospitals,Register,Feedback, LoginForm,Accountform,Accountform1,Changepassword, Requestresetform, Camp
from bloodbank.models import Gallery,Feedback, Hospitals,User,Notification, Campadd,Request
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from random import randint
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
    
@app.route('/',methods=['GET', 'POST'])
@app.route('/index',methods=['GET', 'POST'])
def index():
    form3=Register()
    form1= LoginForm()
    form2=Requestresetform()
    gallery=Gallery.query.all()
    return render_template('index.html',gallery=gallery,form3=form3,form1=form1,form2=form2)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/registeration', methods=['GET','POST'])
def registeration():
    form3=Register()
    form1= LoginForm()
    form2=Requestresetform()
    if form3.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form3.password.data).decode('utf-8')
        new = User(name= form3.name.data,email=form3.email.data,age=form3.age.data, bloodgroup=form3.bloodgroup.data,address=form3.address.data,city=form3.city.data,state=form3.state.data,mobile=form3.mobile.data,password=hashed_password, usertype= 'user' )
        db.session.add(new)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect('/')
    else:
        flash('Registeration unsuccuessful!!! ')
        return redirect('/')
    return render_template('index.html',title='Register', form1=form1,form3=form3,form2=form2)





@app.route('/login', methods=['GET', 'POST'])
def login():
    form3=Register()
    form1 = LoginForm()
    form2=Requestresetform()
    if form1.validate_on_submit():
        user = User.query.filter_by(email=form1.email.data, usertype= 'user').first()
        user1 = User.query.filter_by(email=form1.email.data, usertype= 'admin').first()
        if user and bcrypt.check_password_hash(user.password,form1.password.data):
            print("user")
            login_user(user, remember=form1.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/uindex')
        if user1 and user1.password== form1.password.data:
            login_user(user1, remember=form1.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin')
            
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    else:
        flash('Login Unsuccessful. Please check email and password', 'danger')
        return redirect('/')
    return render_template('index.html', title='Login', form1=form1,form3=form3,form2=form2)








@app.route('/feedback',methods=['GET','POST'])
def feedback():
    if request.method=='POST':
        name= request.form['Name']
        email= request.form['Email']
        phone= request. form['Phone']
        subject= request. form['Subject']
        message= request. form['Message']
        new = Feedback(name=name,email=email,phone=phone,subject=subject,message=message)
        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/')

        except:
            return 'not add'  
    return render_template('index.html')



@app.route('/uindex',methods=['POST','GET'])
@login_required 
def uindex():
    if request.method=='POST':
        name= request.form['Name']
        email= request.form['Email']
        phone= request. form['Phone']
        subject= request. form['Subject']
        message= request. form['Message']
        new = Request(name=name,email=email,phone=phone,subject=subject,message=message)
        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/uindex')

        except:
            return 'not add'  
    else:
        camp=Campadd.query.all()
        gallery=Gallery.query.all()
        return render_template('uindex.html',gallery=gallery,camp=camp)


@app.route('/admin')
@login_required
def admin():
    return render_template("admin.html")

@app.route('/viewimage')
@login_required
def viewimage():
    gallery=Gallery.query.all()
    return render_template('viewimage.html',gallery=gallery)

@app.route('/addimage',methods=['POST','GET'])
@login_required
def addimage():
    form=Addimage()
    if form.validate_on_submit():
        if form.pic.data:
            pic_file = save_picture(form.pic.data)
            view = pic_file
        print(view)  
        gallery = Gallery(name=form.name.data,img=view )
        db.session.add(gallery)
        db.session.commit()
        print(gallery)
        flash('image added')
        return redirect('/viewimage')     
    return render_template('addimage.html',form=form)

@app.route("/imageupdate/<int:id>", methods=['GET', 'POST'])
@login_required
def imageupdate(id):
    gallery = Gallery.query.get_or_404(id)
    form = Addimage()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            gallery.img = picture_file
        gallery.name = form.name.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/viewimage')
    elif request.method == 'GET':
        form.name.data = gallery.name
    image_file = url_for('static', filename='pics/' + gallery.img)
    return render_template('imageupdate.html',form=form)

@app.route("/deleteimage/<int:id>")
@login_required
def deleteimage(id):
    gallery =Gallery.query.get_or_404(id)
    db.session.delete(gallery)
    db.session.commit()
    flash('image has been deleted!', 'success')
    return redirect('/viewimage')


@app.route('/layout')     
def layout():
    form=Accountform()
    return render_template("layout.html",form=form)




@app.route('/publicfeedback')
def publicfeedback():
    feedback = Feedback.query.all()
    return render_template('publicfeedback.html',feedback=feedback)


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def save_picture(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/picture', picture_fn)
    
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



@app.route('/addhospitals',methods=['GET', 'POST'])
@login_required
def addhospitals():
    form=Addhospitals()
    if form.validate_on_submit():
        if form.pic.data:
            pic_file = save_picture(form.pic.data)
            view = pic_file
        print(view)
        hospital = Hospitals(name=form.name.data,place=form.place.data,pincode=form.pincode.data,phone=form.mobile.data,email=form.email.data,availgroup=form.agroup.data,requiredgroup=form.rgroup.data,image=view )
        db.session.add(hospital)
        db.session.commit()
        print(hospital)
        flash('image added')
        return redirect('/adminhospitalview')
            
    return render_template('addhospitals.html',form=form)


@app.route('/adminhospitalview')
@login_required
def adminhospitalview():
    hospital= Hospitals.query.all()
    return render_template('adminhospitalview.html',hospital=hospital)

@app.route("/deletehospital/<int:id>")
@login_required
def deletehospital(id):
    hospital =Hospitals.query.get_or_404(id)
    db.session.delete(hospital)
    db.session.commit()
    flash('hospital has been deleted!', 'success')
    return redirect('/adminhospitalview')

@app.route("/hospitalupdate/<int:id>", methods=['GET', 'POST'])
@login_required
def hospitalupdate(id):
    hospital = Hospitals.query.get_or_404(id)
    form = Addhospitals()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            hospital.image = picture_file
        hospital.name = form.name.data
        hospital.place=form.place.data
        hospital.pincode=form.pincode.data
        hospital.phone=form.mobile.data
        hospital.email=form.email.data
        hospital.availgroup=form.agroup.data
        hospital.requiredgroup=form.rgroup.data
        db.session.commit()
        flash('Hospital has been updated!', 'success')
        return redirect('/adminhospitalview')
    elif request.method == 'GET':
        form.name.data = hospital.name
        form.place.data= hospital.place
        form.pincode.data= hospital.pincode
        form.mobile.data= hospital.phone
        form.email.data= hospital.email
        form.agroup.data= hospital.availgroup
        form.rgroup.data= hospital.requiredgroup
    image_file = url_for('static', filename='picture/' + hospital.image)
    return render_template('hospitalupdate.html',form=form)

@app.route("/account/<int:id>", methods=['GET', 'POST'])
def account(id):
    form = Accountform()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.age = form.age.data
        current_user.address = form.address.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.mobile = form.mobile.data
        db.session.commit() 
        user = User.query.filter_by(email=form.email.data, usertype= 'user').first()
        

    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.age.data = current_user.age
        form.address.data = current_user.address
        form.city.data =  current_user.city
        form.state.data = current_user.state
        form.mobile.data = current_user.mobile

    image_file = url_for('static', filename='picture/' + current_user.image)
    return render_template('account.html', title='Account', image_file=image_file, form=form)




@app.route("/accountadmin/<int:id>", methods=['GET', 'POST'])
def accountadmin(id):
    form = Accountform1()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit() 
        admin = User.query.filter_by(email=form.email.data, usertype= 'admin').first()
        

    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        

    image_file = url_for('static', filename='picture/' + current_user.image)
    return render_template('accountadmin.html', title='Account', image_file=image_file, form=form)




@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    form = Changepassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        logout_user()
        flash('Your Password Has Been Changed')
        return redirect('/login')
    elif request.method == 'GET':
        hashed_password = current_user.password  
    return render_template('changepassword.html', form=form)


@app.route('/adminchangepassword', methods=['GET', 'POST'])
@login_required
def adminchangepassword():
    form = Changepassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        current_user.password = hashed_password
        db.session.commit()
        logout_user()
        flash('Your Password Has Been Changed')
        return redirect('/login')
    elif request.method == 'GET':
        hashed_password = current_user.password  
    return render_template('adminchangepassword.html', form=form)



def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('resettoken', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)




@app.route("/resetrequest", methods=['GET', 'POST'])
def resetrequest():
    form3=Register()
    form1= LoginForm()
    form2=Requestresetform()
    if form2.validate_on_submit():
        user = User.query.filter_by(email=form2.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect('/login')
    return render_template('index.html', title='Reset Password', form3=form3,form1=form1,form2=form2)




@app.route("/resetpassword/<token>", methods=['GET', 'POST'])
def resettoken(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect('/resetrequest')
    form = Changepassword()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect('/login')
    return render_template('resetpassword.html', title='Reset Password', form=form)


@app.route('/notificationadd',methods=['GET', 'POST'])
@login_required
def notificationadd():
    if request.method=='POST':
        notification= request.form['notification']
        mobile= request.form['mobile']
        place = request.form['place']
        
        new = Notification(notification=notification,mobile=mobile,place=place)
        try:
            db.session.add(new)
            db.session.commit()
            return redirect('/notificationview')

        except:
            return 'not add'  
    else:
        return render_template("notificationadd.html")

@app.route('/notificationview')
@login_required
def notificationview():
    noti=Notification.query.all()
    return render_template('notificationview.html',noti=noti)


@app.route("/deletenotification/<int:id>")
@login_required
def deletenotification(id):
    noti =Notification.query.get_or_404(id)
    db.session.delete(noti)
    db.session.commit()
    flash('notification has been deleted!', 'success')
    return redirect('/notificationview')



@app.route('/notificationuser')
@login_required
def notificationuser():
    noti=Notification.query.all()
    return render_template('notificationuser.html',noti=noti)


@app.route('/userview')
@login_required
def userview():
    user=User.query.filter_by(usertype='user').all()
    return render_template('userview.html',user=user)




@app.route('/campadd',methods=['GET', 'POST'])
@login_required
def campadd():
    form = Camp()
    if form.validate_on_submit():
        if form.pic.data:
            pic = save_picture(form.pic.data)
            image = pic
        camp =Campadd(date=form.date.data,description=form.desc.data,mobile=form.mobile.data,place=form.place.data,image=image)
        db.session.add(camp)
        db.session.commit()
        flash('image added')
        return redirect('/campview')

    else:
        return render_template('campadd.html',form=form)
    
@app.route('/campview')
@login_required
def campview():
    camp= Campadd.query.all()
    return render_template('campview.html',camp=camp)


@app.route("/deletecamp/<int:id>")
@login_required
def deletecamp(id):
    camp=Campadd.query.get_or_404(id)
    db.session.delete(camp)
    db.session.commit()
    return redirect('/campview')


@app.route("/campupdate/<int:id>", methods=['GET', 'POST'])
@login_required
def campupdate(id):
    camp = Campadd.query.get_or_404(id)
    form = Camp()
    if form.validate_on_submit():
        if form.pic.data:
            picture_file = save_picture(form.pic.data)
            hospital.image = picture_file
        camp.date = form.date.data
        camp.description=form.desc.data
        camp.mobile=form.mobile.data
        camp.place=form.place.data
        db.session.commit()
        flash('camp has been updated!', 'success')
        return redirect('/campview')
    elif request.method == 'GET':
        form.date.data = camp.date
        form.desc.data= camp.description
        form.mobile.data= camp.mobile
        form.place.data= camp.place
    image_file = url_for('static', filename='picture/' + camp.image)
    return render_template('campupdate.html',form=form)



@app.route('/hospitalview')
@login_required
def hospitalview():
    hosp=Hospitals.query.all()
    return render_template('hospitalview.html',hosp=hosp)

@app.route('/userrequest')
@login_required
def userrequest():
    request=Request.query.all()
    return render_template('userrequest.html',req=request)