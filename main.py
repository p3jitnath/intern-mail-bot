field = 'Computer Vision'

import scraper
scraper.create_mailing_list(field)

import email_handler
email_handler.send_emails(field)