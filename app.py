from flask import Flask, render_template, Response, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from models import ContactForm, db, LoginForm, Member
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import URL
import logging

logging.basicConfig(filename='./example.log', encoding='utf-8',filemode='w', level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

url_object = URL.create(
    "mysql+pymysql",
    username="tzdsba2zu3camqhu",
    password="xpeacc27rod5t4sg",
    host="q0h7yf5pynynaq54.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    database="zqpvmdfskjzainuf",
    port=3306
)

app = Flask(__name__)
ckeditor = CKEditor(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = url_object
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

new_admin = Member(name='admin',
                   user='yano79',
                   password=generate_password_hash("admin3%&79","pbkdf2",8))
# hy7g%0}\@sxD)
# name="admin",
#                    email="yano79@aol.com",


db.init_app(app)
# with app.app_context():
    # db.session.query(Member).delete()
    # db.drop_all()
    # db.create_all()
    # db.session.add(new_admin)
    # db.session.commit()
    # articles = db.session.query(Member).all()

@login_manager.user_loader
def load_user(user_id):
    return Member.query.get(int(user_id))

@app.route('/robots.txt')
def noindex():
    r = Response(response="User-Agent: *\nDisallow: /\n", status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r


@app.route('/')
def home():  # put application's code here
    return render_template("index.html")


@app.route('/documents')
@login_required
def documents():
    return render_template("documents.html")


@app.route('/experience')
def experience():
    return render_template("experience.html")


@app.route('/references')
def references():
    return render_template("references.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_id = login_form.user.data
        user_pwd = login_form.password.data
        user = Member.query.where(Member.user == user_id)
        try:
            if check_password_hash(user[0].password, user_pwd):
                login_user(user[0])
                return redirect(url_for('documents'))
        except IndexError:
            flash('Email and/or password incorrect. Please Try again')
            return redirect(url_for('login'))
    return render_template('login.html', form=login_form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/contact', methods=["GET", "POST"])
def contact():
    new_form = ContactForm()
    if new_form.validate_on_submit():
        name = new_form.name.data
        email = new_form.email.data
        message = new_form.message.data
        text = f"{name}\n{email}\n{message}"
        new_form.email_notification(text=text)
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", form=new_form)


@app.route('/gallery')
def gallery():
    return render_template("gallery.html")


if __name__ == '__main__':
    app.run(debug=True)
