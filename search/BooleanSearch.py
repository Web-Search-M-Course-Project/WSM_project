import json
from utlis import preprocess, middle_to_after, st

class BooleanSearch:
    def __init__(self):
        with open('./data/inverted_index.json', 'r', encoding='utf-8') as f:
            self.posting_lists = json.load(f)
        with open('./data/meta_data.json', 'r', encoding='utf-8') as f:
            self.meta_data = json.load(f)

    def search(self, query):
        expression = middle_to_after(query)
        modified_expression = []
        for item in expression:
            if item not in ['NOT', 'AND', 'OR']:
                item = st.stem(item)
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
        for i in range(len(result)):
            uid = result[i]
            result[i] = self.meta_data[uid]
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


