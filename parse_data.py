from concurrent.futures import process
from curses import meta
import json
import os
from sys import meta_path
from importlib_metadata import metadata
import numpy as np
import pandas as pd
from tqdm import tqdm


def process_data(folders, pmc=False):
    metadata = pd.read_csv(
        "./2020-04-03/metadata.csv", encoding="utf-8")
    metadata.head()
    all_papers = {}

    no_cord_uid_pmc = []
    no_cord_uid = []
    multi_cord_uid_pmc = []
    multi_cord_uid = []

    for folder in folders:
        count = 0
        print(f"current folder: {folder}")
        for file_name in tqdm(os.listdir(folder)):
            file_name = os.path.join(folder, file_name)
            with open(file_name) as f:
                data = json.loads(f.read())
            
            # json: sha/pmcid, metadata(title, authors), filename
            # metadata: cord_uid, abstract, 

            paper = {}
            paper['metadata'] = data['metadata']
            paper["paper_id"] = data['paper_id']
            paper['filename'] = file_name 

            # if not pmc:
            #     query = f"sha == '{data['paper_id']}'"
            # else:
            #     query = f"pmcid == '{data['paper_id']}'"
            # res = metadata.query(query)

            res = metadata[metadata['sha' if not pmc else 'pmcid'].str.contains(data['paper_id'])==True]
            cord_uid = res['cord_uid'].values
            abstract = res['abstract'].values

            paper['cord_uid'], paper['abstract'] = None, None

            if len(cord_uid) == 0:
                count += 1
                if not pmc: no_cord_uid.append(data['paper_id'])
                else: no_cord_uid_pmc.append(data['paper_id'])
                if count <= 100:
                    print('============no cord uid===============')
                    print(data['paper_id'])
                continue

            elif len(cord_uid) > 1:
                if not pmc: multi_cord_uid.append(data['paper_id'])
                else: multi_cord_uid_pmc.append(data['paper_id'])
                print('===========multiple cord uid==============')
                print(data['paper_id']) 
                continue

            else:
                cord_uid = cord_uid[0]
                paper['cord_uid'] = cord_uid[0]
                paper['abstract'] = abstract[0]
            
            all_papers[cord_uid] = paper
            
        print(f'folder {folder} done')

    store_file = './data/brief_data.json' if not pmc else './data/brief_data_pmc.json'
    aux_file = './data/auxilary_info.json' if not pmc else './data/auxilary_info_pmc.json'
    with open(store_file, "w", encoding="utf-8") as f:
        json.dump(all_papers, f, indent=5, ensure_ascii=False)
    
    other_info = {
        'no_cord_uid': no_cord_uid,
        'no_cord_uid_pmc': no_cord_uid_pmc,
        'multi_cord_uid': multi_cord_uid,
        'multi_cord_uid_pmc': multi_cord_uid_pmc
    }

    with open(aux_file, 'w', encoding="utf-8") as f:
        json.dump(other_info, f, indent=4, ensure_ascii=False)

    print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nprievious folder: {folder}\n!!!!!!!!!!!!!!')


# folders = ['2020-04-03/biorxiv_medrxiv/pdf_json', 
#             '2020-04-03/comm_use_subset/pdf_json', 
#             '2020-04-03/custom_license/pdf_json', 
#             '2020-04-03/noncomm_use_subset/pdf_json']
# folders_pmc = ['2020-04-03/comm_use_subset/pmc_json',
#                 '2020-04-03/noncomm_use_subset/pmc_json',
#                 '2020-04-03/custom_license/pmc_json']

# process_data(folders)
# process_data(folders_pmc, pmc=True)            

def simplify_data(file, meta_data={}):
    with open(file, 'r', encoding='utf-8') as f:
        all_data = json.load(f)
        for (uid, paper) in tqdm(all_data.items()):
            title = paper['metadata']['title']
            abstract = paper['abstract']
            authors = paper['metadata']['authors']
            filename = paper['filename']
            paper_id = paper['paper_id']
            meta_data[uid] = {'title': title, 'abstract': abstract, 'authors': authors,
            'filename':filename, 'paper_id':paper_id}
    
    return meta_data

pdf_file = './data/brief_data.json'
pmc_file = './data/brief_data_pmc.json'

meta_data = simplify_data(pdf_file)
meta_data = simplify_data(pmc_file, meta_data)

with open('./data/meta_data.json', 'w', encoding="utf-8") as f:
    json.dump(meta_data, f, indent=5, ensure_ascii=False)


# metadata = pd.read_csv(
#     "./2020-04-03/metadata_with_mag_mapping_04_03.csv", encoding="utf-8")
# metadata.head()

# # find by paper id
# res = metadata[metadata['sha'].str.contains("beb38f99a59fa3129e34eadfc28c9d46438ec820")==True]
# # res = metadata.query("sha == 'beb38f99a59fa3129e34eadfc28c9d46438ec820'")
# print(res)

# cord_id = res['cord_uid'].values
# # cord_id = res['cord_uid'].astype(str)
# print(cord_id, type(cord_id))
