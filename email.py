from flask_mail import Message
from app import mail
from flask import url_for

def send_activation_email(user):
    token = user.confirm_token
    msg = Message('Account Activation', sender='noreply@militia.com', recipients=[user.email])
    msg.body = f'''To activate your account, visit the following link:{url_for ('activate', token=token, _external=True)}

Dear Applicant,

We are thrilled to welcome you to our esteemed military organization. 
Your decision to join us is a testament to your commitment, courage, and dedication to serving our nation. 
As you embark on this honorable journey, you will undergo rigorous training, develop invaluable skills, and forge bonds with fellow servicemen and women who share your sense of duty. 
We are confident that your unique talents and unwavering spirit will contribute significantly to our mission of protecting and defending our country. 
Welcome to the team, and thank you for your willingness to serve.
'''
    mail.send(msg)
