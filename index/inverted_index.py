import sys
import os
import json
import pickle
import pandas as pd
from tqdm import tqdm


cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, ".."))
from utils import preprocess


def construct_inverted_index_from_metadata(fussy_method=None):
    metadata = pd.read_csv("./2020-04-03/metadata.csv", encoding="utf-8")
    # with open('./data/meta_data.json', 'r', encoding='utf-8') as f:
    #     meta_data = json.load(f)

    inverted_index_map = {}
    for idx, paper in tqdm(metadata.iterrows()):
    # for cord_uid, paper in tqdm(meta_data.items()):
        cord_uid = paper['cord_uid']
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
    with open(f'./data/inverted_index_{fussy_method}.pkl', 'wb') as f:
        pickle.dump(inverted_index_map, f)


def construct_inverted_index(fussy_method=None):
    with open('./data/meta_data.json', encoding='utf-8') as f:
        all_data = json.load(f)

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
    # construct_inverted_index_from_metadata(fussy_method='none')
    # construct_inverted_index(fussy_method='stem')
    # construct_inverted_index(fussy_method='lemmatize')

    # construct_inverted_index_from_metadata(fussy_method=None)
    # construct_inverted_index_from_metadata(fussy_method='stem')
    construct_inverted_index_from_metadata(fussy_method='lemmatize')