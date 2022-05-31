import json
import sys
import os
from textblob import Word
import pickle
import pandas as pd

cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, ".."))
from utils import preprocess, middle_to_after, st

class FussySearch:
    def __init__(self, fussy_method='stem'):
        assert fussy_method in ['stem', 'lemmatize']
        self.fussy_method = fussy_method
        with open(f'./data/position_index_{fussy_method}.pkl', 'rb') as f:
            self.posting_lists = pickle.load(f)

        # self.metadata = pd.read_csv("./2020-04-03/metadata.csv", encoding="utf-8")
        with open(f'./data/meta_data.json', 'r', encoding='utf-8') as f:
            self.metadata = json.load(f)           
    
    def __list_author(self, authors, num=5):
        """return author name under each paper"""
        names = []
        count = 0
        for author in authors:
            count += 1
            name = ""
            if len(author['first'])!=0: name = author['first'][0] 
            # if len(author['middle']) != 0: name += author['middle'][0][0] 
            if len(author['last'])!=0: name = name + ' ' + author['last'] 
            if len(name)!= 0: names.append({'name':name, 'show':count<=num}) 
        return names

    def search(self, query):
        results_all = []
        expression = middle_to_after(query)
        fussy_expression = []
        modified_expression = []
        for item in expression:
            if item not in ['NOT', 'AND', 'OR']:
                if self.fussy_method == 'stem':
                    item = st.stem(item)
                elif self.fussy_method == 'lemmatize':
                    item = Word(item).lemmatize()
                    item = Word(item).lemmatize('v')
                fussy_expression.append(item)
                item = set(self.posting_lists[item].keys())
            modified_expression.append(item)

        stack_value = []
        for idx, item in enumerate(modified_expression):
            if item in ['NOT', 'AND', 'OR']:
                n2 = stack_value.pop()
                n1 = stack_value.pop()
                result = n1
                if item == 'NOT':
                    result -= n2
                elif item == 'AND':
                    result &= n2
                elif item == 'OR':
                    result |= n2
                stack_value.append(result)
            else:
                stack_value.append(item)  # 词语直接压栈
        result = list(stack_value[0])        
        # print(result)
        for i in range(len(result)):
            uid = result[i]
            positions = []
            for item in fussy_expression:
                try:
                    positions += self.posting_lists[item][uid] 
                except:  # NOT xxx / OR xxx
                    # print('cannot find', item)
                    pass

            # paper = self.metadata[self.metadata.cord_uid == uid].to_dict('records')[0]
            paper = self.metadata.get(uid, None)
            if not paper:
                continue
            
            authors = self.__list_author(paper['authors'])
            abstract = preprocess(paper['abstract'], fussy_method=self.fussy_method)
            cur_res = {'cord_uid':uid, 'title': paper['title'], 
                        'authors': authors, 
                        'abstract': abstract, 'positions': positions}
            results_all.append(cur_res)
            # print(result[i])
        return results_all

if __name__ == '__main__':
    fussy_search = FussySearch(fussy_method='stem')
    query = "Strain AND Identification OR network"
    print('Query: ', query)
    fussy_search.search(query)
    # print("====================================================================")
    # query = "Strain AND Identification OR network NOT automated"
    # print('Query: ', query)
    # fussy_search.search(query)
    # print("###############################################################")
    
    # fussy_search = FussySearch(fussy_method='lemmatize')
    # query = "Strain AND Identification OR network"
    # print('Query: ', query)
    # fussy_search.search(query)
    # print("====================================================================")
    # query = "Strain AND Identification OR network NOT automated"
    # print('Query: ', query)
    # fussy_search.search(query)


