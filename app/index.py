import math
from flask import Flask, render_template, request
from flask_sqlalchemy import Pagination
from controller import get_result, slice_result


app = Flask(__name__)

@app.route('/')
def main_index():
    return "hello! The server is running!"

@app.route('/search/')
def search_engine():
    return render_template('search.html')

@app.route('/result/', methods=['GET'])
def do_search():
    per_page_num, total = 5, 30
    key = request.args['searchText']
    results_all = get_result(search_text=key, num=total)

    page = request.args.get('page', default=1, type=int)
    
    current_page = Pagination(results_all, page, 
        per_page=per_page_num, total=len(results_all), 
        items=slice_result(results_all, page, per_page_num))

    return render_template('result.html', searchText=key, paginate=current_page)

if __name__ == "__main__":
    app.run(debug=True, port=3333)