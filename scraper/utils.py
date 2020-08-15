import requests
import re
from bs4 import BeautifulSoup

from .skrapp import retrieve_email

GOOGLE_SCHOLAR_URL = "http://scholar.google.com"
AUTHOR_URL = GOOGLE_SCHOLAR_URL + "/citations?hl=en&user={}"
LIMIT = 5

headers = {'User-Agent': 'Mozilla/5.0', 'Referer': GOOGLE_SCHOLAR_URL}
session = requests.session()

def to_dict(author_obj):
    del author_obj['nav']
    del author_obj['_sections']
    del author_obj['_filled']
    return author_obj

def get_soup_object(url):
    page = session.get(url, headers=headers, allow_redirects=True)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup, page

def extract_home_page(author_id):
    try:
        author_soup, _ = get_soup_object(AUTHOR_URL.format(author_id))
        home_page_url = author_soup.find('div', {"id": "gsc_prf_ivh"}).find('a', {"class": "gsc_prf_ila"}).get('href')
        return home_page_url   
    except:
        return None

def extract_top_publications(author_id, text_summarizer):
    author_soup, _ = get_soup_object(AUTHOR_URL.format(author_id))
    results = []; ctr = 0
    for row in author_soup.findAll('tr', {"class": "gsc_a_tr"}):
        if (ctr == LIMIT):
            break
        try:
            publication_name = row.find('a', {"class": "gsc_a_at"}).text
            publication_soup, _ = get_soup_object(GOOGLE_SCHOLAR_URL + row.find('a', {"class": "gsc_a_at"}).get('data-href'))        
            publication_description = publication_soup.find('div', {"class": "gsh_small"}).text

            if text_summarizer:
                publication_description_summary = text_summarizer.generate_summary(publication_description)
            else:
                publication_description_summary = None

            if len(publication_description) < 100:
                raise Exception
            
            publication_gs_url = publication_soup.find('div', {"class": "gsc_vcd_merged_snippet"}).find('div').find('a').get('href')
            _ , page = get_soup_object(publication_gs_url)
            results.append({
                "name": publication_name, 
                "url": page.url,
                "description": publication_description,
                "summary": publication_description_summary
            })
            ctr += 1
        except:
            continue

    return results

def get_details(person, text_summarizer=None):
    person['homepage'] = extract_home_page(person['id'])
    publication = extract_top_publications(person['id'], text_summarizer)
    person['publications'] = []
    person['publications'].append(publication)
    person['email'] = retrieve_email(person['name'], person['email'])
    return person