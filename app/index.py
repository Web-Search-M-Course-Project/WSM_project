import math, os, sys, json
from flask import Flask, render_template, request
from flask_sqlalchemy import Pagination
from importlib_metadata import metadata
from controller import get_full_paper, slice_result, get_result_from_query

cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, ".."))
# from utils import preprocess, middle_to_after, st

app = Flask(__name__)


@app.route('/')
def main_index():
    return "hello! The server is running!"

@app.route('/search/')
def search_engine():
    return render_template('search.html')

@app.route('/error/')
def error():
    return render_template('error.html')

@app.route('/result/', methods=['GET'])
def do_search():
    # try:
    per_page_num, total = 5, 30
    key = request.args['searchText']
    fussy_method = request.values.get('fussy')
    sort_method = request.values.get('sort')
    # fussy_method = request.args.get('Fussy',None) # stem, lemmatize, None
    # sort_method = request.args.get('mix', None) # tfidf, cos-tf, citation, pagerank, norm1, mix
    results_all_sorted = get_result_from_query(key, fussy_method, sort_method)

    # results_all = get_result(search_text=key, search=fussy_search, meta_data=meta_data, num=5)
    page = request.args.get('page', default=1, type=int)
    current_page = Pagination(results_all_sorted, page, 
        per_page=per_page_num, total=len(results_all_sorted), 
        items=slice_result(results_all_sorted, page, per_page_num))
    # except:
    #     return render_template('error.html')

    return render_template('result.html', searchText=key, paginate=current_page, fussy=fussy_method, sort=sort_method)

@app.route('/paper/',  methods=['GET'])
def show_paper():
    try:
        uid = request.args['uid']
        result = get_full_paper(uid)
    except:
        render_template('error.html')
    return render_template('paper.html', res=result, uid=uid)



if __name__ == "__main__":
    app.run(debug=True, port=3333)