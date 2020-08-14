from utils import get_soup_object, extract_home_page, extract_top_publications
from scholarly import scholarly
import json

LIMIT = 2
search_query = scholarly.search_author('Deep Learning')


def to_dict(author_obj):
    del author_obj['nav']
    del author_obj['_sections']
    del author_obj['_filled']
    return author_obj

def search_by_id(collection, id):
    return list(filter(lambda person: person['id'] == id, collection))

ctr = 0
while True: 
    try: 
        professor = next(search_query) 
        with open('./records/mailing_list.json', 'r') as file:
            collection = json.load(file)

        professor = to_dict(professor.__dict__)
        print(professor['id'])

        if len(search_by_id(collection, professor['id'])) == 0:
            professor['homepage'] = extract_home_page(professor['id'])
            publication = extract_top_publications(professor['id'])
            professor['publications'] = []
            professor['publications'].append(publication)
            collection.append(professor)
            with open('./records/mailing_list.json', 'w') as file:
                json.dump(collection, file)
            ctr += 1
        
        if (ctr == 2):
            break

    except StopIteration: 
        break


