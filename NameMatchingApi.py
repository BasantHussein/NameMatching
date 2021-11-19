import json

from flask import Flask, jsonify
import NameMatching_f

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Search the name you want.'})


@app.route('/search/<target>', methods=["GET"])
def search(target):
    json_strings = [json.dumps(json_obj, ensure_ascii=False) for json_obj in NameMatching_f.NameMatching(target).keys()]

    return str(json_strings)


if __name__ == '__main__':
    app.run()
