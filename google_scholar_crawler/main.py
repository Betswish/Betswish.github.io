from scholarly import scholarly
import jsonpickle
import json
from datetime import datetime
import os

author: dict = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
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
from semanticscholar import SemanticScholar
sch = SemanticScholar()
author_semantic = sch.get_author(2112611646)

shieldio_data_semantic = {
  "schemaVersion": 1,
  "label": "citations_semantic",
  "message": f"{author_semantic.citationCount}",
}
with open(f'results/gs_data_shieldsio_semantic.json', 'w') as outfile:
    json.dump(shieldio_data_semantic, outfile, ensure_ascii=False)
