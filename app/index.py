from flask import Flask, render_template, request
from controller import get_result

app = Flask(__name__)

@app.route('/')
def main_index():
    return "hello! The server is running!"

@app.route('/search/')
def search_engine():
    return render_template('search.html')

@app.route('/result/', methods=['GET'])
def do_search():
    key = request.args['searchText']
    results = get_result(search_text=key)
    return render_template('result.html', searchText=key, results=results)

if __name__ == "__main__":
    app.run(debug=True, port=3333)