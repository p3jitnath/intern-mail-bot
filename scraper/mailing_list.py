from .utils import get_details, to_dict
from scholarly import scholarly
import json

import sys
sys.path.append("../")

from text_processing import AbstractiveTextSummarizer


LIMIT = 5

def search_by_id(collection, id):
    return list(filter(lambda person: person['id'] == id, collection))

def create_mailing_list(category):
    search_query = scholarly.search_author(category)
    category_filename = category.lower().replace(' ', '_')
    ctr = 0

    text_summarizer = AbstractiveTextSummarizer()

    while True: 
        try: 
            professor = next(search_query) 
            try:
                with open('./records/mailing_list_{}.json'.format(category_filename), 'r') as file:
                    collection = json.load(file)
            except FileNotFoundError:
                collection = []

            professor = to_dict(professor.__dict__)
            print("Getting : Prof. {} ...".format(professor['name']))

            if len(search_by_id(collection, professor['id'])) == 0:
                professor = get_details(professor, text_summarizer)
                collection.append(professor)
                with open('./records/mailing_list_{}.json'.format(category_filename), 'w') as file:
                    json.dump(collection, file)
                ctr += 1
                print("Status: Completed")
            else:
                print("Status: Already Scraped")
            
            if (ctr == LIMIT):
                break

        except StopIteration: 
            break


