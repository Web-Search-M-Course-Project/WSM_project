from time import sleep
import dataset.dataall as dt
import dataset
import utlis
import json
import os
import numpy as np
"""
# data = dt.data_all()
# data = dt.data_cached()
"""

a = dataset.light.dataset()

"""
initialize the data using the following methods 
"""
if False:
    a.init(fussy_method="lemmatize")
    a.citation_init(fussy_method="lemmatize")
    exit(0)

if False:
    a.pagerank_init()
    exit(0)
    pass


"""
_summary_
"""
with utlis.timer("preprocess cold start") as t:
    utlis.preprocess("hello world",fussy_method="lemmatize")

with utlis.timer("dataset cold start") as t:
    a.load_dataset(fussy_method="lemmatize")

with utlis.timer("query time") as t:
    b, query = (a.query_to_list("teeth macrocyclic health"))
    # b, query = (a.query_to_list("teeth macrocyclic"))
    # print(b)

with utlis.timer("get title") as t:
    title = a.list_of_id_to_name(b)

with utlis.timer("get tfidf score") as t:
    score = a.list_of_tf_idf(b, query, scorer=dataset.light.tfidf_score.tfidf())
    # print(score)
    assert(len(score) == len(title))
    __order = a.zipper2(b,title,score)[:5]
    print(json.dumps(__order,indent=4))
    

with utlis.timer("get cosine tfidf score") as t:
    score = a.list_of_cosine_tf_idf(b, query, scorer=dataset.light.tfidf_score.tfidf())
    assert(len(score) == len(title))
    __order = a.zipper2(b,title,score)[:5]
    print(json.dumps(__order,indent=4))

with utlis.timer("get cosine norm-1 score") as t:
    # score = a.list_of_tf_idf(b, query, scorer=dataset.light.tfidf_score.tfidf())
    score = a.list_of_cosine_norm1(b, query, scorer=dataset.light.tfidf_score.cosine())
    assert(len(score) == len(title))
    __order = a.zipper2(b,title,score)[:5]
    print(json.dumps(__order,indent=4))

with utlis.timer("get cosine norm-2 score") as t:
    # score = a.list_of_tf_idf(b, query, scorer=dataset.light.tfidf_score.tfidf())
    score = a.list_of_cosine(b, query, scorer=dataset.light.tfidf_score.cosine())
    assert(len(score) == len(title))
    __order = a.zipper2(b,title,score)[:5]
    print(json.dumps(__order,indent=4))

with utlis.timer("get citation score") as t:
    score = a.list_of_citations(b)
    assert(len(score)==len(title))
    __order = a.zipper2(b,title,score)[:5]
    print(json.dumps(__order,indent=4))

with utlis.timer("get pagerank score") as t:
    score = a.list_of_pagerank(b)
    assert(len(score)==len(title))
    __order = a.zipper2(b,title,score)[:5]
    print(json.dumps(__order,indent=4))
    pass

with utlis.timer("get mixed score") as t:
    score_pagerank = a.list_of_pagerank(b)
    score_citation = a.list_of_citations(b)
    score_tfidf = a.list_of_tf_idf(b, query, scorer=dataset.light.tfidf_score.tfidf())
    score_costf = a.list_of_cosine_tf_idf(b, query, scorer=dataset.light.tfidf_score.tfidf())
    scores = np.array([score_costf,score_citation,score_pagerank,score_tfidf],dtype = np.float64)
    scores = scores - np.mean(scores, axis = 1, keepdims = True)
    scores = scores / np.sqrt(np.var(scores, axis = 1, keepdims = True)) * np.array([10.0, 1.0, 1.0, 1.0]).reshape((-1,1))
    print(scores.mean(axis = 1))
    print(scores.var(axis = 1))
    score = list(scores.mean(axis = 0))
    __order = a.zipper2(b,title,score)[:5]
    print(json.dumps(__order,indent=4))
    pass


t = None

