from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Userform
# from forms import 

app = Flask(__name__)
app.config['SQLACLHEMY_DATABASE_URI'] = 'postresql:///auth_auth_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'abc123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():

    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    form = Userform()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password)

        db.session.add(new_user)
        session['username'] = new_user.username
        return redirect('/secret')

    return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login_user():
    form = Userform()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f'Welcome, {user,username}!', 'primary')
            session['user_id'] = user.id
            return redirect('/secret')

@app.route('/secret')
def secret_page():
    if user:
        session['user_id'] = user.id
        return render_template('/secret')