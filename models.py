import smtplib
from email.mime.text import MIMEText
from flask_login import UserMixin
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from flask_sqlalchemy import SQLAlchemy




MY_EMAIL = "aureliano.basso@gmail.com "
PASSWORD = "loggnutchvjfvzbg"

db = SQLAlchemy()

class ContactForm(FlaskForm):
    name = StringField(label='Full name:', validators=[DataRequired(), Length(max=50)])
    email = EmailField(label='Email Address:', validators=[DataRequired(), Length(max=100), Email()])
    phone = StringField(label='Phone Number: (optional)')
    message = CKEditorField(label='Your message:', validators=[DataRequired(), Length(max=5000)])
    submit = SubmitField('Send')

    def email_notification(self, text: str):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
            connection.connect("smtp.gmail.com", 465)
            connection.login(user=MY_EMAIL, password=PASSWORD)
            subject = "Potential employer enquiry !!!!!"
            sender = "aureliano.basso@gmail.com"
            recipients = (
                "aureliano.basso@gmail.com"
            )
            Ccopies = ""
            body = text
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = sender
            msg["To"] = recipients
            msg["Cc"] = Ccopies
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=msg["To"].split(",") + msg["Cc"].split(","),
                msg=f"Subject: {subject}\n\n" + body)


class LoginForm(FlaskForm):
    user = StringField(label='USER :', validators=[DataRequired(), Length(max=100)])
    password = PasswordField(label='PASSWORD :', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')

class Member(UserMixin, db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    user = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))


    def is_active(self):
        self.is_active = True
        return self.is_active

    def is_anonymous(self):
        self.is_anonymous = False
        return self.is_anonymous

    def is_authenticated(self):
        self.is_authenticated = True
        return self.is_authenticated