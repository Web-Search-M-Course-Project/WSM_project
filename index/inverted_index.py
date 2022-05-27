import json
import sys
sys.path.append("..")
from utlis import preprocess
import pandas as pd
import pickle
from tqdm import tqdm

def construct_inverted_index_from_metadata(fussy_method=None):
    # print("nothing OK")
    metadata = pd.read_csv("../2020-04-03/metadata_with_mag_mapping_04_03.csv", encoding="utf-8")
    # print("Open OK")
    inverted_index_map = {}
    for idx, paper in tqdm(metadata.iterrows()):
        cord_uid = paper['cord_uid']
        paper_id = paper['sha']
        title = preprocess(paper['title'], fussy_method=fussy_method)
        abstract = preprocess(paper['abstract'], fussy_method=fussy_method)
        tokens = title + abstract
        # print(tokens)
        for token in tokens:
            if token in inverted_index_map.keys():
                posting_list = inverted_index_map[token]
                if cord_uid in posting_list.keys():
                    inverted_index_map[token][cord_uid] += 1
                else:
                    inverted_index_map[token][cord_uid] = 1
            else:
                inverted_index_map[token] = {cord_uid: 1}
    # print(inverted_index_map)
    # print("OK")
    with open(f'../data/inverted_index_{fussy_method}.pkl', 'wb') as f:
        pickle.dump(inverted_index_map, f)


def construct_inverted_index(fussy_method=None):
    # print("nothing OK")
    with open('./data/data.json', encoding='utf-8') as f:
        all_data = json.load(f)
    # print("Open OK")
    inverted_index_map = {}
    for paper in all_data:
        paper_id = paper['paper_id']
        title = preprocess(paper['metadata']['title'], fussy_method=fussy_method)
        if len(paper['abstract']):
            abstract = preprocess(paper['abstract'][0]['text'])
        else:
            abstract = []
        tokens = title + abstract
        # print(tokens)
        for token in tokens:
            if token in inverted_index_map.keys():
                posting_list = inverted_index_map[token]
                if paper_id in posting_list.keys():
                    inverted_index_map[token][paper_id] += 1
                else:
                    inverted_index_map[token][paper_id] = 1
            else:
                inverted_index_map[token] = {paper_id: 1}
    # print(inverted_index_map)
    # print("OK")
    with open(f'./data/inverted_index_{fussy_method}.json', 'w', encoding='utf-8') as f:
        json.dump(inverted_index_map, f,  indent=4, ensure_ascii=False)

if __name__ == '__main__':
    construct_inverted_index_from_metadata(fussy_method='none')
    # construct_inverted_index(fussy_method='stem')
    # construct_inverted_index(fussy_method='lemmatize')