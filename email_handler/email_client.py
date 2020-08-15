import smtplib, ssl

import os
import configparser

path_current_directory = os.path.dirname(__file__)
path_config_email_file = os.path.join(path_current_directory, '../config', 'email.ini')

config = configparser.ConfigParser()
config.read(path_config_email_file)

password = config['User']['password']
sender_email = config['User']['sender_email']
port = config['GMAIL']['port']
smtp_server = config['GMAIL']['smtp_server']

class EmailClient():
    def __init__(self):
        self.port = port
        self.smtp_server = smtp_server
        self.password = password
        self.sender_email = sender_email
        
    def send(self, message="", receiver_email=None):
        if receiver_email == None:
            receiver_email = self.sender_email
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context=ssl.create_default_context()) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, receiver_email, message.encode("utf8"))
            server.quit()


