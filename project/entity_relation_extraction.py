import gzip

import re
from bs4 import BeautifulSoup
from bs4.element import Comment

import pandas as pd
import wikipedia as wk
import spacy  

from search import LocalSearch



KEYNAME = "WARC-TREC-ID"

# initialize language model
nlp = spacy.load("en_core_web_md")
entity_link_cache = {}


#Function to get only visible text in HTML - From https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
def tag_visible(element):
    #Filter elements with following tags
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    #Filter comments
    if isinstance(element, Comment):
        return False
    return True


def get_text(html, flag):
	soup = BeautifulSoup(html, "html5lib")  #Extract HTMLContent
	if flag == 1:
		value = soup.find("span", {"property" : "dbo:abstract", "xml:lang":"en"})
		if value is not None:
			value = value.getText()
		else:
			value = ''
	else:
		plain_text = soup.findAll(text=True) #Get plain text
		value = filter(tag_visible, plain_text) #Get only visible text
		#Format the text		
		value = " ".join(value) 
		value = re.sub(r'[^\x00-\x7F]+',' ', value) #Replace special unicode characters
		value = re.sub(r'[(?<=\{)(:*?)(?=\})]', ' ', value) #Replace special characters
		value = ' '.join(value.split())

	return value


# The goal of this function process the webpage and returns a list of labels -> entity ID
def extract_text_from_warc(payload):
    if payload == '':
        return

    key = None
    for line in payload.splitlines():
        if line.startswith(KEYNAME):
            key = line.split(': ')[1]
            break

            
    #Check if the WARC block contains HTML code
    if key and ('<html' in payload):
        html = payload.split('<html')[1]
        value = get_text(html, 0)
        yield (key, value)



def extract_entities(text):

    doc = nlp(text)
    entities = []

    # consider entity types to reduce entities being generate by spacy
    # https://www.kaggle.com/code/curiousprogrammer/entity-extraction-and-classification-using-spacy
    entity_types = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT']
    for entity in doc.ents: 
        if (entity.label_ in entity_types):
            entities.append(entity)

    return entities


def getContentFromLink(link):
	try:
		linkText = wk.page(link, auto_suggest=False).content.lower()
	except wk.exceptions.DisambiguationError as e:
		options = filter(lambda x: "(disambiguation)" not in x, e.options)
		linkText = wk.page(options[0], auto_suggest=False).content.lower()
	return linkText


# The goal of this function is to find relations between the entities
def find_relations(payload, entities):
    if payload == '':
        return

    key = None
    for line in payload.splitlines():
        if line.startswith(KEYNAME):
            key = line.split(': ')[1]
            break

    # A simple solution would be to extract the text between two previously
    # extracted entitites, and then determine if it is a valid relation

    # Optionally, we can try to determine whether the relation mentioned in the
    # text refers to a known relation in Wikidata.

    # Similarly as before, now we are cheating by reading a set of relations
    # from a file. Clearly, this will report the same set of relations for each page
    tokens = [line.split('\t') for line in open('data/sample-relations-cheat.txt').read().splitlines()]
    for label, subject_wikipedia_id, object_wikipedia_id, wikidata_rel_id in tokens:
        if key:
            yield key, subject_wikipedia_id, object_wikipedia_id, label, wikidata_rel_id


def split_records(stream):
    payload = ''
    for line in stream:
        if line.strip() == "WARC/1.0":
            yield payload
            payload = ''
        else:
            payload += line
    yield payload

if __name__ == '__main__':
    import sys
    
    '''
    try:
        _, INPUT = sys.argv
    except Exception as e:
        print('Usage: python3 starter-code.py INPUT')
        sys.exit(0)
    '''

    INPUT = "./data/warcs/sample.warc.gz"

    i = 0

   
    with gzip.open(INPUT, 'rt', errors='ignore') as fo:
        for record in split_records(fo):


            for key, text in extract_text_from_warc(record):        
                entities = extract_entities(text)

                # Entity Linking
                # extracting text of entity from spacys output
                entities_str = list(map(lambda x: str(x.text), entities))
                # For each document extract entities and save the potential wikipedia candidate entities to dictionary(entity_link_cache)
                for entity in entities:
                    try:
                        links = wk.search(entity.text)
                        entity_link_cache[entity.text] = [(l, getContentFromLink(l)) for l in links]
                    except Exception as e:
                        pass    
                
                searchAgent = LocalSearch(entities_str, entity_link_cache)
                result = searchAgent.runLocalSearch(1)
                print(result)

                
                # TODO : Relation Extraction
                

    print(entity_link_cache)


  









