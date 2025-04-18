from scholarly import scholarly
import jsonpickle
import json
from datetime import datetime
import os

# Google Scholar
# API
author_id=os.environ['GOOGLE_SCHOLAR_ID']
author: dict = scholarly.search_author_id(author_id)
print('Data scratched')
scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
name = author['name']
author['updated'] = str(datetime.now())
author['publications'] = {v['author_pub_id']:v for v in author['publications']}
print(json.dumps(author, indent=2))
os.makedirs('results', exist_ok=True)
with open(f'results/gs_data.json', 'w') as outfile:
    json.dump(author, outfile, ensure_ascii=False)

shieldio_data = {
  "schemaVersion": 1,
  "label": "citations",
  "message": f"{author['citedby']}",
}
with open(f'results/gs_data_shieldsio.json', 'w') as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False)

# Semantic Scholar
import requests
from bs4 import BeautifulSoup

# Version 1: with Semantic Scholar API
from semanticscholar import SemanticScholar
sch = SemanticScholar()
author_semantic = sch.get_author(2112611646)
citation_num = author_semantic.citationCount

# Version 2: with HTML request
# url="https://www.semanticscholar.org/author/Jirui-Qi/2112611646"
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'}
# html=requests.get(url,headers=headers)
# val = BeautifulSoup(html.text, 'html.parser')
# citation_num = val.find_all("span", class_="author-detail-card__stats-row__value")[-2].text

# Format
shieldio_data_semantic = {
  "schemaVersion": 1,
  "label": "citations_semantic",
  "message": f"{citation_num}",
}
with open(f'results/gs_data_shieldsio_semantic.json', 'w') as outfile:
    json.dump(shieldio_data_semantic, outfile, ensure_ascii=False)
