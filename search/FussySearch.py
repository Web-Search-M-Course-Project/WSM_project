import json
import sys
sys.path.append("..")
from utlis import preprocess, middle_to_after, st
from textblob import Word
import pickle
import pandas as pd

class FussySearch:
    def __init__(self, fussy_method='stem'):
        assert fussy_method in ['stem', 'lemmatize']
        self.fussy_method = fussy_method
        with open(f'../data/position_index_{fussy_method}.pkl', 'rb') as f:
            self.posting_lists = pickle.load(f)
        self.metadata = pd.read_csv("../2020-04-03/metadata_with_mag_mapping_04_03.csv", encoding="utf-8")

    def search(self, query):
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
            paper = self.metadata[self.metadata.cord_uid == uid].to_dict('records')[0]
            result[i] = {'cord_uid':uid, 'title': paper['title'], 
                        'authors': paper['authors'], 'abstract': paper['abstract'], 'positions': positions}
            print(result[i])


        return result

if __name__ == '__main__':
    fussy_search = FussySearch(fussy_method='stem')
    query = "Strain AND Identification OR network"
    print('Query: ', query)
    fussy_search.search(query)
    print("====================================================================")
    query = "Strain AND Identification OR network NOT automated"
    print('Query: ', query)
    fussy_search.search(query)
    print("###############################################################")
    fussy_search = FussySearch(fussy_method='lemmatize')
    query = "Strain AND Identification OR network"
    print('Query: ', query)
    fussy_search.search(query)
    print("====================================================================")
    query = "Strain AND Identification OR network NOT automated"
    print('Query: ', query)
    fussy_search.search(query)


