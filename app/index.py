import math, os, sys, json
from flask import Flask, render_template, request
from flask_sqlalchemy import Pagination
from importlib_metadata import metadata
from controller import get_result, slice_result, list_author

cur_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cur_dir, ".."))
# from utils import preprocess, middle_to_after, st
from search.FussySearch import FussySearch

app = Flask(__name__)
fussy_search = FussySearch(fussy_method='stem')
file_path = './data/meta_data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    meta_data = json.load(f)

@app.route('/')
def main_index():
    return "hello! The server is running!"

@app.route('/search/')
def search_engine():
    return render_template('search.html')

@app.route('/paper/')
def error():
    return render_template('error.html')

@app.route('/result/', methods=['GET'])
def do_search():
    try:
        per_page_num, total = 5, 30
        key = request.args['searchText']

        results_all = fussy_search.search(key)

        # results_all = get_result(search_text=key, search=fussy_search, meta_data=meta_data, num=5)

        page = request.args.get('page', default=1, type=int)
        current_page = Pagination(results_all, page, 
            per_page=per_page_num, total=len(results_all), 
            items=slice_result(results_all, page, per_page_num))
    except:
        return render_template('error.html')

    return render_template('result.html', searchText=key, paginate=current_page)

@app.route('/paper/',  methods=['GET'])
def show_paper():
    uid = request.args['uid']
    result = meta_data[uid]
    result['authors'] = list_author(result['authors'])
    return render_template('paper.html', res=result, uid=uid)



if __name__ == "__main__":
    app.run(debug=True, port=3333)