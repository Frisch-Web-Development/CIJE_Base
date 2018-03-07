from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from data import resource
from data import resources_list

import secret
from model import *

print(resources_list.jewish_resources)

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


@app.route('/getlocations', methods=["GET"])
def getLocations():
    ls = Location.query.all()
    return jsonify([s.serialize for s in ls])


@app.route('/getlocation/<int:lid>', methods=["GET"])
def getLocation(lid):
    l = Location.query.filter_by(id=lid).first()
    if l is not None:
        return jsonify(l.serialize)
    return "ERROR"


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


if __name__ == "__main__":
    port = 5000
    app.run(host='0.0.0.0', port=port)

