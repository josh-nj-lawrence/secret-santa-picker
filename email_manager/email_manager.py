import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailManager:
    """
    EmailManager class instantiated to send emails from configured email address.

    Usage:
        emailer = EmailManager()
        pwd = input("Enter password: ")

        emailer.config(
            "myemail@gmail.com",
            pwd,
        )

        emailer.send_email(
            "myfriend@gmail.com",
            "Secret Santa",
            "You are the secret santa for ..."
    """
    def __init__(self):
        self.email = None
        self.password = None
        self.server = "smtp.gmail.com"
        self.port = None
        self.context = None
        self.encrypt_protocol = None
        self.configured = False
    
    
    # Setters
    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password = password

    def set_server(self, server):
        self.server = server

    def set_port(self, port):
        self.port = port

    def set_context(self):
        self.context = ssl.create_default_context()
    
    def set_encrypt_protocol(self, proto):
        if proto.upper() in ["SSL", "TLS"]:
            self.encrypt_protocol = proto
        else:
            raise ValueError("Protocol must be SSL or TLS")

    def set_configured(self):
        if not self.configured:
            self.configured = True
        else:
            raise ValueError("EmailManager already configured")

    # Action methods
    def config(self, email, password, encrypt_protocol="TLS"):
        try:
            self.set_encrypt_protocol(encrypt_protocol)
            self.config_port()
            self.set_email(email)
            self.set_password(password)
            self.set_context()
        except:
            raise ValueError("Error configuring EmailManager")

    def config_port(self):
        if self.encrypt_protocol == "SSL":
            self.set_port(465)
        elif self.encrypt_protocol == "TLS":
            self.set_port(587)
        else:
            raise ValueError("Protocol must be SSL or TLS")

    # EmailManager methods
    def create_message(self, subject, body):
        return f"Subject: {subject}\n\n{body}"
    
    def send_email(self, recipient_email, subject, body):
        if self.encrypt_protocol == "SSL":
            self._send_email_ssl(recipient_email, subject, body)
        elif self.encrypt_protocol == "TLS":
            self._send_email_tls(recipient_email, subject, body)
        else:
            raise ValueError("Email not sent correctly.")
        
    def _send_email_ssl(self, recipient_email, subject, body):
        with smtplib.SMTP_SSL(self.server, self.port, context=self.context) as server:
            server.login(self.email, self.password)
            server.sendmail(self.email, recipient_email, self.create_message(subject, body))

    def _send_email_tls(self, recipient_email, subject, body):
        with smtplib.SMTP(self.server, self.port) as server:
            server.ehlo()
            server.starttls(context=self.context)
            server.ehlo()
            server.login(self.email, self.password)
            server.sendmail(self.email, recipient_email, self.create_message(subject, body))

if __name__ == """__main__""":
    emailer = EmailManager()

    # Read password for secret file
    with open("password.txt", mode='r') as f:
        pwd = f.read()

    emailer.config(
        "youremail@gmail.com",
        pwd
    )

    # Plain text email
    emailer.send_email(
        "recipientemail@gmail.com", 
        "TESTING APP CONN", 
        "Hello, this is a test email from python."
    )

    # MIMEMultipart email
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = emailer.email
    message["To"] = "recipientemail@gmail.com"

    text = """\
    Hello,
    This is a test email from python.""" 
    
    html = """\
    <html>
    <body>
        <p>Hi,
        This is a test email from python. 
        </p>
    </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    emailer.send_email(
        message["To"],
        message["Subject"],
        message.as_string()
    )
