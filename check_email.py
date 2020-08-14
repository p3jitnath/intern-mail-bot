from email_handler import EmailClient, compose_email
import configparser
import csv

config = configparser.ConfigParser()
config.read("config/email.ini")

password = config['User']['password']
sender_email = config['User']['sender_email']
port = config['GMAIL']['port']
smtp_server = config['GMAIL']['smtp_server']

email_client = EmailClient(port, smtp_server, password, sender_email)

with open('config/subject.txt') as subject_file:
    subject = subject_file.read()

with open('config/introduction.txt') as introduction_file:
    introduction = introduction_file.read()

with open('config/body.txt') as body_file:
    body = body_file.read()

with open('config/signature.txt') as signature_file:
    signature = signature_file.read()

with open('config/attachment_links.txt') as attachment_links_file:
    attachment_links = attachment_links_file.read()   

with open('records/mailing_list.csv') as mailing_list:
    mailing_list_reader = csv.DictReader(mailing_list, delimiter=',', skipinitialspace=True)
    for row in mailing_list_reader:
        row = dict(row)
        receiver_email = row['email']
        last_name = row['last_name']
        message = compose_email(last_name, subject, introduction, body, signature, attachment_links)
        email_client.send(receiver_email, message)
