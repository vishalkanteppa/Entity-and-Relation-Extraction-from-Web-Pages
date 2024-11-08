# Entity and Relation Extraction from Web Pages

## Overview
This project implements an entity and relation extraction engine that processes web pages in WARC format to recognize entities, link them to Wikipedia pages, and identify relations between them, linking these relations to Wikidata properties where possible. The program receives a collection of web pages, extracts entities and relationships, and outputs results in a predefined format.

## Input and Output
### Input
- A WARC file containing web pages, with each page having a unique ID (`WARC-TREC-ID`)

### Output
- Entities - Each identified entity from a page is output in the following format:

`ENTITY: <page_id>TAB<entity mention>TAB<wikipedia (en) URL>`

- Relations - Relationships between entities on each page are output as:

`RELATION: <page_id>TAB<wikipedia (en) URL (subject)>TAB<wikipedia (en) URL (object)>TAB<text that describes the relation>TAB<url of the wikidata relation (optional)>`

## Approach
1. Entity Recognition and Linking - Entities are detected using NLP techniques, linking each recognized entity to its corresponding Wikipedia URL.
2. Relation Extraction - Using dependency parsing, we identify and categorize relations between entities, linking relations to Wikidata properties when feasible for extra credit.
3. Evaluation - The extraction results are evaluated using precision, recall, and F1 score to benchmark accuracy.
