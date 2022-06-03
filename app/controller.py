import json
import os
import sys
import math
from tqdm import tqdm
from Data_process import Author, list_author
import random



cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, ".."))
from search.FussySearch import FussySearch
from search.BooleanSearch import BooleanSearch
from light import dataset
from utils import preprocess

lemmaSearch = FussySearch(fussy_method='lemmatize')
stemSearch = FussySearch(fussy_method='stem')
Boolean = BooleanSearch()

DataSorter_stem = dataset(fussy_method='stem')
DataSorter_lemmatize = dataset(fussy_method='lemmatize')

file_path = './data/meta_data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    meta_data = json.load(f)


def path_changer(path):
    # from 2020-04-03/noncomm_use_subset/pmc_json/PMC6522884.xml.json
    #  -->"./data_all/comm_use_subset/pdf_json/000b7d1517ceebb34e1e3e817695b6de03e2fa78.json" 
    new_path = './data_all' + path[10:]
    return new_path


def list_author(authors):
    """return author name under each paper"""
    names = []
    count = 0
    for author in authors:
        count += 1
        name = ""
        if isinstance(author, str):
            names.append(author)
            continue
        if len(author['first'])!=0:  name = author['first']
        if len(author['middle']) != 0: 
            for mid in author['middle']:
                name += mid
        if len(author['last'])!=0: name = name + ' ' + author['last'] 
        if len(name)!= 0: names.append(name) 
        if count >= 5:
            break
    return names


def slice_result(results, page_num, per_page_num):
    if page_num < 1 or page_num > math.ceil(len(results) /per_page_num):
        page_num = 1
    start, end = (page_num - 1)*per_page_num, page_num*per_page_num
    return results[start:end]


def get_full_paper(uid):
    result = meta_data[uid]
    result['authors'] = list_author(result['authors'])
    return result


def get_result_from_uid(result_with_positions, fussy_method):
    results_all = []
    for uid, positions in result_with_positions.items():
    # for uid in uids:
        paper = meta_data.get(uid, None)
        if not paper:
            continue
        authors = list_author(paper['authors'])
        abstract = preprocess(paper['abstract'], fussy_method=fussy_method)
        title_processed = preprocess(paper['title'], fussy_method=fussy_method)
        positions = [i-len(title_processed) for i in positions if i>len(title_processed)]
        
        cur_res = {'cord_uid':uid, 'title': paper['title'], 
                    'authors': authors, 
                    'abstract': abstract, 'positions': positions, 'filename': paper['filename']}
        results_all.append(cur_res)
    return results_all


def get_result_from_query(query, fussy_method='stem', sort_method='mix'):
    if fussy_method == 'stem':
        results_with_positions = stemSearch.search(query)
        DataSorter = DataSorter_stem
    elif fussy_method == 'lemmatize':
        results_with_positions = lemmaSearch.search(query)
        DataSorter = DataSorter_lemmatize
    else:
        results_with_positions = Boolean.search(query)
        DataSorter = DataSorter_stem

    results_all = get_result_from_uid(results_with_positions, fussy_method=fussy_method)
    sorted_results = DataSorter.cal_score(results_all, query, method=sort_method)

    return sorted_results






                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
