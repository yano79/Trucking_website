import smtplib
from email.mime.text import MIMEText

from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email

MY_EMAIL = "aureliano.basso@gmail.com "
PASSWORD = "loggnutchvjfvzbg"


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
