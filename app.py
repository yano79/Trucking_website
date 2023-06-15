from flask import Flask, render_template, Response
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor

from models import ContactForm

app = Flask(__name__)
ckeditor = CKEditor(app)
Bootstrap(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = url_object
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


@app.route('/robots.txt')
def noindex():
    r = Response(response="User-Agent: *\nDisallow: /\n", status=200, mimetype="text/plain")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r


@app.route('/')
def home():  # put application's code here
    return render_template("index.html")


@app.route('/documents')
def documents():
    return render_template("documents.html")


@app.route('/experience')
def experience():
    return render_template("experience.html")


@app.route('/references')
def references():
    return render_template("references.html")


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
