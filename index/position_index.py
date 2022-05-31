import json
import sys
import os

import pandas as pd
import pickle
from tqdm import tqdm
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, ".."))
from utils import preprocess

def construct_position_index_from_metadata(fussy_method=None):
    metadata = pd.read_csv("./2020-04-03/metadata.csv", encoding="utf-8")
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
    with open(f'./data/position_index_{fussy_method}.pkl', 'wb') as f:
        pickle.dump(position_index_map, f)

def find_pos(text, expression):
    res = []
    for item in expression:
        if item not in ['NOT', 'AND', 'OR']:
            pos = re.search(item, text).span()
            res.append(pos)
    return res


if __name__ == '__main__':
    construct_position_index_from_metadata(fussy_method=None)
    construct_position_index_from_metadata(fussy_method='stem')
    construct_position_index_from_metadata(fussy_method='lemmatize')