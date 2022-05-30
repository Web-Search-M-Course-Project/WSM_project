import json
from utils import preprocess

def construct_inverted_index(fussy_method=None):
    with open('../data.json', encoding='utf-8') as f:
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
        print(tokens)
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

    with open(f'inverted_index_{fussy_method}.json', 'w', encoding='utf-8') as f:
        json.dump(inverted_index_map, f,  indent=4, ensure_ascii=False)

if __name__ == '__main__':
    construct_inverted_index(fussy_method='none')
    construct_inverted_index(fussy_method='stem')
    construct_inverted_index(fussy_method='lemmatize')