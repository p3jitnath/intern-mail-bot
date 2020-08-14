from .utils import get_soup_object, extract_home_page, extract_top_publications
from scholarly import scholarly
import json

LIMIT = 2

def to_dict(author_obj):
    del author_obj['nav']
    del author_obj['_sections']
    del author_obj['_filled']
    return author_obj

def search_by_id(collection, id):
    return list(filter(lambda person: person['id'] == id, collection))

def create_mailing_list(category):
    search_query = scholarly.search_author(category)
    category_filename = category.lower().replace(' ', '_')
    ctr = 0
    while True: 
        try: 
            
            professor = next(search_query) 

            try:
                with open('./records/mailing_list_{}.json'.format(category_filename), 'r') as file:
                    collection = json.load(file)
            except FileNotFoundError:
                collection = []

            professor = to_dict(professor.__dict__)
            print("Getting : Prof. {}".format(professor['name']))

            if len(search_by_id(collection, professor['id'])) == 0:
                professor['homepage'] = extract_home_page(professor['id'])
                publication = extract_top_publications(professor['id'])
                professor['publications'] = []
                professor['publications'].append(publication)
                collection.append(professor)
                with open('./records/mailing_list_{}.json'.format(category_filename), 'w') as file:
                    json.dump(collection, file)
                ctr += 1
            
            if (ctr == LIMIT):
                break

        except StopIteration: 
            break


