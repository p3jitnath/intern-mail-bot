import smtplib, ssl

class EmailClient():
    def __init__(self, port, smtp_server, password, sender_email):
        self.port = port
        self.smtp_server = smtp_server
        self.password = password
        self.sender_email = sender_email
        
    def send(self, receiver_email, message=""):
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=ssl.create_default_context()) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, message)
            server.quit()


