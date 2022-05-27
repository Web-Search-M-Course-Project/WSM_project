import json
import sys
sys.path.append("..")
from utlis import preprocess
import pandas as pd
import pickle
from tqdm import tqdm
import re

def construct_position_index_from_metadata(fussy_method=None):
    metadata = pd.read_csv("../2020-04-03/metadata_with_mag_mapping_04_03.csv", encoding="utf-8")
    # print("Open OK")
    position_index_map = {}
    for idx, paper in tqdm(metadata.iterrows()):
        cord_uid = paper['cord_uid']
        paper_id = paper['sha']
        title = preprocess(paper['title'], fussy_method=fussy_method)
        abstract = preprocess(paper['abstract'], fussy_method=fussy_method)
        tokens = title + abstract
        # print(tokens)
        for idx, token in enumerate(tokens):
            if token in position_index_map.keys():
                posting_list = position_index_map[token]
                if cord_uid in posting_list.keys():
                    position_index_map[token][cord_uid].append(idx)
                else:
                    position_index_map[token][cord_uid] = [idx]
            else:
                position_index_map[token] = {cord_uid: [idx]}
    # print(inverted_index_map)
    # print("OK")
    with open(f'../data/position_index_{fussy_method}.pkl', 'wb') as f:
        pickle.dump(position_index_map, f)

def find_pos(text, expression):
    res = []
    for item in expression:
        if item not in ['NOT', 'AND', 'OR']:
            pos = re.search(item, text).span()
            res.append(pos)
    return res


if __name__ == '__main__':
    # construct_position_index_from_metadata(fussy_method='none')
    # construct_position_index_from_metadata(fussy_method='stem')
    construct_position_index_from_metadata(fussy_method='lemmatize')