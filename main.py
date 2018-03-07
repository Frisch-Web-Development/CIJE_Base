from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

import secret

import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = secret.serverURL

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "Flask WebApp"
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route("/")
def hello():
    return render_template('main.html')


@app.route("/loginform")
def loginform():
    return render_template('login.html', invalid=False)


@app.route('/login', methods=['GET','POST'])
def login():
    lemail = request.form['email']
    lpw = request.form['password']
    result = User.query.filter_by(email=lemail, password=lpw).first()
    if result is not None:
        login_user(result)
        return redirect("/")
    else:
        return render_template('login.html', invalid=True)


@app.route('/information', methods=['GET', 'POST'])
def info():
    return render_template('info.html', invalid=True, cat="Cello", dog="world")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/signupform')
def signupform():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup():
    existingusers = User.query.filter_by(email=request.form['email']).all()
    if len(existingusers) > 0:
        return "You are already signed up"
    r = Role.query.filter_by(name='User').first()
    newuser = User(first_name=request.form['fname'], last_name=request.form['lname'], email=request.form['email'], password=request.form['password'], role=r.id)
    db.session.add(newuser)
    db.session.commit()
    login_user(newuser)
    return redirect("/")


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64), unique=False, index=True)
    last_name = db.Column(db.String(64), unique=False, index=True)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password = db.Column(db.String(64), unique=False, index=True)
    is_active = True

    def __repr__(self):
        return '<User %r>' % self.email


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
