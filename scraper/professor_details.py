from scholarly import scholarly
from .utils import get_details, to_dict

import json

import sys
sys.path.append("../")

from text_processing import AbstractiveTextSummarizer
text_summarizer = AbstractiveTextSummarizer()

def extract_professor_details(name):
    
    search_query = scholarly.search_author(name)
    author = next(search_query) 
    author = to_dict(author.__dict__)

    print("Getting : Prof. {} ...".format(author['name']))

    author = get_details(author, text_summarizer)

    author_file_name = author['name'].lower().replace(' ', '_')
    with open("./records/authors/{}.json".format(author_file_name), 'w') as file: # Check
        json.dump(author, file)

    print("Status: Completed")