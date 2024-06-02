from flask import render_template, url_for, flash, redirect, request
from app import app, db, mail
from forms import RegistrationForm, LoginForm
from models import User
from flask_mail import Message
import secrets

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.confirm_token = secrets.token_urlsafe(16)
        db.session.add(user)
        db.session.commit()
        send_activation_email(user)
        flash('An activation email has been sent to your email address.', 'info')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if user.confirmed:
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Please confirm your email address.', 'warning')
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/activate/<token>")
def activate(token):
    user = User.query.filter_by(confirm_token=token).first_or_404()
    user.confirmed = True
    user.confirm_token = None
    db.session.commit()
    flash('Your account has been activated!', 'success')
    return redirect(url_for('login'))

def send_activation_email(user):
    token = user.confirm_token
    msg = Message('Account Activation', sender='noreply@militia.com', recipients=[user.email])
    msg.body = f'''To activate your account, visit the following link:
{url_for('activate', token=token, _external=True)}

Dear Applicant,

We are thrilled to welcome you to our esteemed military organization. 
Your decision to join us is a testament to your commitment, courage, and dedication to serving our nation. 
As you embark on this honorable journey, you will undergo rigorous training, develop invaluable skills, and forge bonds with fellow servicemen and women who share your sense of duty. 
We are confident that your unique talents and unwavering spirit will contribute significantly to our mission of protecting and defending our country. 
Welcome to the team, and thank you for your willingness to serve.
'''
    mail.send(msg)
