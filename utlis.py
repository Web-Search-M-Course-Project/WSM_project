from nltk import tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
from textblob import Word

st = PorterStemmer()

english_stopwords = stopwords.words('english')
english_punctuations = "[,.:+-/;?()&!*@#$%\'\"]"

def preprocess(text, fussy_method=None):
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
