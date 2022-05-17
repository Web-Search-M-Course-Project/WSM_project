import json
import tarfile
import numpy as np
import pandas as pd
from tqdm import tqdm

# #%%
#
# metadata = pd.read_csv("2020-04-03/metadata_with_mag_mapping_04_03.csv", encoding="utf-8")
# metadata.head()
#
# #%%
#
# # find by paper id
# metadata.query("sha == 'f056da9c64fbf00a4645ae326e8a4339d015d155'")
#
# #%%
#
# # find by title
# metadata.query("title == 'SIANN: Strain Identification by Alignment to Near Neighbors'")
#
# #%% md
#
# tar = tarfile.open("2020-04-03/biorxiv_medrxiv.tar.gz", "r:gz")
# all_data = []
# for tarinfo in tqdm(tar):
#     if tarinfo.isreg():
#         f = tar.extractfile(tarinfo.name)
#         data = json.loads(f.read())
#         all_data.append(data)
#         print(data)
#
# with open('data.json', "w", encoding="utf-8") as f:
#         json_str = json.dump(all_data, f, indent=4, ensure_ascii=False)

meta_data = {}
with open('./data/data.json', "r", encoding="utf-8") as f:
    all_data = json.load(f)
    for paper in all_data:
        paper_id = paper['paper_id']
        title = paper['metadata']['title']
        if len(paper['abstract']):
            abstract = paper['abstract'][0]['text']
        else:
            abstract = []
        meta_data[paper_id] = {'title': title, 'abstract': abstract}

with open('./data/meta_data.json', "w", encoding="utf-8") as f:
    json.dump(meta_data, f, indent=4, ensure_ascii=False)