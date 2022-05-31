import json
import sys
import os
import pandas as pd
import pickle
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, ".."))
from utils import middle_to_after

class BooleanSearch:
    def __init__(self):
        with open('./data/position_index_none.pkl', 'rb') as f:
            self.posting_lists = pickle.load(f)
        self.metadata = pd.read_csv("./2020-04-03/metadata.csv", encoding="utf-8")

    def search(self, query):
        expression = middle_to_after(query)
        modified_expression = []
        for item in expression:
            if item not in ['NOT', 'AND', 'OR']:
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
        print(result)
        for i in range(len(result)):
            uid = result[i]
            positions = []
            for item in expression:
                if item not in ['NOT', 'AND', 'OR']:
                    try:
                        positions += self.posting_lists[item][uid] 
                    except:  # NOT xxx / OR xxx
                        # print('cannot find', item)
                        pass
            paper = self.metadata[self.metadata.cord_uid == uid].to_dict('records')[0]
            result[i] = {'cord_uid':uid, 'title': paper['title'], 
                        'authors': paper['authors'], 'abstract': paper['abstract'], 
                        'positions': positions}
            print(result[i])

        return result

if __name__ == '__main__':
    bool_search = BooleanSearch()
    query = "Strain AND Identification OR network"
    print('Query: ', query)
    bool_search.search(query)
    print("====================================================================")
    query = "Strain AND Identification OR network NOT automated"
    print('Query: ', query)
    bool_search.search(query)


