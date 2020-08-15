from datetime import datetime
from glob import glob

import json

from .email_client import EmailClient
from . import template

email_client = EmailClient()
already_sent_emails = glob("./records/emails/*.txt")

def compose_email(professor, field):

    header = template.header.format(date=datetime.utcnow(), field=field)
    subject = template.subject.format(professor['name'])
    publications_str = """"""

    for i, publication in enumerate(professor['publications']):
        publication_str = template.publication.format(
            ctr = i + 1,
            publication_name = publication['name'],
            publication_url = publication['url'],
            abstract_summary = publication['summary']
        )
        publications_str += publication_str

    professor_str = template.professor.format(
        gs_id = professor['id'],
        name = professor['name'],
        affiliation = professor['affiliation'],
        email_id = professor['email'],
        interests = ', '.join(professor['interests']),
        cited_count = professor['citedby'],
        publications = publications_str
    )

    return str(subject + header + professor_str + template.signature)


def send_emails(field):

    field_file_name = field.lower().replace(" ", "_")

    with open("./records/mailing_list_{}.json".format(field_file_name), 'r') as file:
        collection = json.load(file)

    for professor in collection:
        print("Email for Prof.{}".format(professor['name']))
        email_file_name = professor['name'].lower().replace(" ", "_").replace('.', '')

        if ("./records/emails/" + email_file_name + ".txt") in already_sent_emails:
            print("Status: Already Sent")
            continue

        message = compose_email(professor, field)
        email_client.send(message)
        with open("./records/emails/{}.txt".format(email_file_name), 'w') as email_file:
            email_file.write(message)
            print("Status: Sent")

