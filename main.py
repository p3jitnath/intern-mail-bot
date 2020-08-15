import scraper
import email_handler

field = 'Computer Vision'
scraper.create_mailing_list(field)
email_handler.send_emails(field)