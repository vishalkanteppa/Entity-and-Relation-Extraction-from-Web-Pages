raw_text = "Tony Stark was the CEO of Stark Industries"
entities_of_interest = ["ORGANIZATION", "PERSON", "LOCATION", "CITY", "STATE_OR_PROVINCE", "COUNTRY"]

# Load spacy model
import spacy
nlp = spacy.load("en_core_web_sm")  

# Apply spacy model to raw text (to split to sentences, tokenize, extract entities etc.)
doc = nlp(raw_text)  

# Load pre-trained SpanBERT model
from spanbert import SpanBERT 
spanbert = SpanBERT("./pretrained_spanbert")  

# Extract relations
from spacy_help_functions import extract_relations
relations = extract_relations(doc, spanbert, entities_of_interest)
print("Relations: {}".format(dict(relations)))
for k,v in relations.items():
    entity1 = '_'.join(k[0].split(' '))
    entity2 = '_'.join(k[2].split(' '))
    relation = k[1].split(':')[1]
    print(f"RELATION: https://en.wikipedia.org/wiki/{entity1} https://en.wikipedia.org/wiki/{entity2} {relation}")