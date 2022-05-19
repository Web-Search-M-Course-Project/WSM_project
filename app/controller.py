import json
import os
import math
from tqdm import tqdm
from Data_process import Author, list_author
import random

dir = '2020-04-03/comm_use_subset/pdf_json'
# file = './2020-04-03/comm_use_subset/pdf_json/0a00a6df208e068e7aa369fb94641434ea0e6070.json'


def get_result(search_text, num=5):
    dir = '2020-04-03/comm_use_subset/pdf_json'
    files = os.listdir(dir)
    all_files = random.choices(files, k=num)
    all_files = [os.path.join(dir, i) for i in all_files]
    results = parse_result(all_files)
    return results

def slice_result(results, page_num, per_page_num):
    if page_num < 1 or page_num > math.ceil(len(results) /per_page_num):
        page_num = 1
    start, end = (page_num - 1)*per_page_num, page_num*per_page_num
    return results[start:end]
    

def parse_result(files):
    results = []
    for file in files:
        with open(file) as f:
            data = json.load(f)

        authors = list_author(data['metadata']['authors'])
        title = data['metadata']['title']
        abstract = data['abstract'][0]['text'] if len(data['abstract']) >0 else ""
        abstract = abstract[:500]+'..' if len(abstract) > 500 else abstract
        result = {'authors': authors, 'title': title, 'abstract': abstract}
        results.append(result)
    return results
        

# count = 1
# for file in tqdm(os.listdir(dir)):
#     file = os.path.join(dir, file)
#     with open(file) as f:
#         data = json.load(f)
    
#     for author in data['metadata']['authors']:
#         print(Author(author))
#     count += 1
#     # if count >= 100:
#     #     break

#     # test list_author method:
#     # authors = list_author(data['metadata']['authors'])
#     # print(authors)






                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
