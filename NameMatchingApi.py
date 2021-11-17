from flask import Flask, jsonify
import NameMatching_f

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Search the name you want.'})


@app.route('/search/<target>', methods=["GET"])
def search(target):
    return NameMatching_f.NameMatching(target)


if __name__ == '__main__':
    app.run()
