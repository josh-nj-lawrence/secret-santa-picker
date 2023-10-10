import email_manager

emailer = email_manager.EmailManager()
with open("passwordfile.txt", mode='r') as f:
    password = f.read()

print("Configuring emailer...")
emailer.config(
    email="myemail@gmail.com",
    password=password
)

print("Sending email...")
emailer.send_email(
    recipient_email="friendsemail@gmail.com",
    subject="THIS IS PYTHON",
    body="This is a test. I send this email with python, how does it look? Normal? I hope so!"
)