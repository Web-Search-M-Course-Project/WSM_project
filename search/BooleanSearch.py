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
        with open('./data/position_index_None.pkl', 'rb') as f:
            self.posting_lists = pickle.load(f)
  
    def search(self, query):
        result_with_positions = {}
        expression = middle_to_after(query)
        modified_expression = []
        for item in expression:
            if item not in ['NOT', 'AND', 'OR']:
                item = item.lower()
                item = set(self.posting_lists.get(item, {}).keys())
                # item = set(self.posting_lists[item].keys())
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
            result_with_positions[uid] = positions
        return result_with_positions

if __name__ == '__main__':
    bool_search = BooleanSearch()
    query = "Strain AND Identification OR network"
    print('Query: ', query)
    bool_search.search(query)
    print("====================================================================")
    query = "Strain AND Identification OR network NOT automated"
    print('Query: ', query)
    bool_search.search(query)


