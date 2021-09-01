import smtplib
from email.mime.text import MIMEText


def send_mail(customer, dealer, rating, comments):
    port = 2525
    smtp_server = "smtp.mailtrap.io"
    login = "4138afbbf6a12b"
    password = "8391dfa5a1b406"
    message = f"<h3>New Feedback Submission<h3><ul><li>Customer: {customer}</li><li>Customer: {dealer}</li><li>Customer: {rating}</li><li>Customer: {comments}</li></ul>"

    sender_email = "cornishglamour@gmail.com"
    receiver_email = "cornishglamour@gmail.com"
    msg = MIMEText(message, "html")
    msg["Subject"] = "Lexus Feedback"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
