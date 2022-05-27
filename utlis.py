from nltk import tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
from textblob import Word
import pickle
import json
import os

def picklize():
    _dir = os.listdir("data")
    for dd in _dir:
        if not os.path.isfile(os.path.join("data",dd.split(".")[0]+".pkl")):
            print("G: ", os.path.join("data",dd.split(".")[0]+".pkl"))
            jsonfile = open(os.path.join("data",dd), "r", encoding='utf-8')
            pklfile = open(os.path.join("data",dd.split(".")[0]+".pkl"), "wb")
            all_data = json.load(jsonfile)
            pickle.dump(all_data, pklfile)
            pklfile.close()
        if not os.path.isfile(os.path.join("data",dd.split(".")[0]+".json")):
            print("G: ", os.path.join("data",dd.split(".")[0]+".json"))
            jsonfile = open(os.path.join("data",dd.split(".")[0]+".json"), "w", encoding='utf-8')
            pklfile = open(os.path.join("data",dd), "rb")
            all_data = pickle.load(pklfile)
            json.dump(all_data, jsonfile, indent = 4)
            jsonfile.close()
            
            # with open('./data/data.json', "r", encoding="utf-8") as f:
            #     all_data = json.load(f)

st = PorterStemmer()

english_stopwords = stopwords.words('english')
english_punctuations = "[,.:+-/;?()&!*@#$%\'\"]"

def preprocess(text, fussy_method=None):
    try:
        text = re.sub(english_punctuations, "", text)
        text = re.sub("[0-9]", "", text)
        tokens = tokenize.word_tokenize(text)
        filtered_tokens = [word for word in tokens if word not in english_stopwords]
        processed_text = filtered_tokens
        if fussy_method == 'stem':
            processed_text = [st.stem(word) for word in processed_text]
        elif fussy_method == 'lemmatize':
            processed_text = [Word(word).lemmatize() for word in processed_text]
            processed_text = [Word(word).lemmatize('v') for word in processed_text]
    except:
        processed_text = []

    return processed_text

#  中缀表达式转化后缀表达式
def middle_to_after(s):
    ops_rule = {
        'NOT': 0,
        'AND': 1,
        'OR': 2
    }
    expression = []
    ops = []
    ss = s.split(' ')
    for item in ss:
        if item in ['AND', 'NOT', 'OR']:  # 操作符
            while len(ops) >= 0:
                if len(ops) == 0:
                    ops.append(item)
                    break
                op = ops.pop()
                if op == '(' or ops_rule[item] > ops_rule[op]:
                    ops.append(op)
                    ops.append(item)
                    break
                else:
                    expression.append(op)
        elif item == '(':  # 左括号，直接入操作符栈
            ops.append(item)
        elif item == ')':  # 右括号，循环出栈道
            while len(ops) > 0:
                op = ops.pop()
                if op == '(':
                    break
                else:
                    expression.append(op)
        else:
            expression.append(item)  # 词语，直接入表达式栈

    while len(ops) > 0:
        expression.append(ops.pop())

    return expression
