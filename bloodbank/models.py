from bloodbank import db,login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    age = db.Column(db.Integer)
    bloodgroup = db.Column(db.String(80))
    address = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    mobile = db.Column(db.Integer)
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    usertype = db.Column(db.String(80))

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.name}', '{self.password}','{self.email}', '{self.image}','{self.usertype}')"

class Gallery(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.VARCHAR)
    img = db.Column(db.String(20), nullable=False, default='default.jpg')

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.VARCHAR)
    email= db.Column(db.VARCHAR)
    phone= db.Column(db.Integer)
    subject= db.Column(db.VARCHAR)
    message= db.Column(db.VARCHAR)
    usertype= db.Column(db.VARCHAR)

class Hospitals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    place= db.Column(db.String)
    pincode= db.Column(db.Integer)
    phone= db.Column(db.Integer)
    email = db.Column(db.String(120))
    availgroup= db.Column(db.String(120))
    requiredgroup= db.Column(db.String(120))
    image = db.Column(db.String(20), nullable=False, default='default.jpg')

class Notification(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    notification = db.Column(db.String(200))
    mobile = db.Column(db.Integer)
    place = db.Column(db.String(200))
class Campadd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date= db.Column(db.String(50))
    description= db.Column(db.String(50))
    mobile = db.Column(db.Integer)
    place = db.Column(db.String(200))
    image = db.Column(db.String(20), nullable=False, default='default.jpg')

