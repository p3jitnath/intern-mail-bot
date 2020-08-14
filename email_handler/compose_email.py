

def compose_email(last_name, subject, introduction, body, signature, attachment_links=""):
    subject = "Subject: {}".format(subject) + '\n\n'
    salutation = "Dear Professor {},".format(last_name) + '\n'
    introduction = '\n' + introduction + '\n'
    body = '\n' + body + '\n'
    signature = '\n\n' + signature

    if len(attachment_links) != 0:
        attachment_links = '\n' + attachment_links

    return (subject + salutation + introduction + body + signature + attachment_links)