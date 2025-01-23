from django.core.mail import send_mail

def send_token_email(user_email, token):
    subject = "Your Document Viewer Login Token"
    message = f"Use this token to log in: {token}"
    send_mail(subject, message, 'shedrackamodu5@gmail.com', [user_email])
