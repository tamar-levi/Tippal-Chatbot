from flask import Flask, request, jsonify
from queries import query_res
from data_from_the_user import insert_to_index
from flask_cors import CORS

# Initializing flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])


@app.route('/query', methods=['POST'])
def get_req_res():
    try:
        request_data = request.get_json()
        res = query_res(request_data["query"])
        return jsonify({'result': res}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/insert', methods=['POST'])
def insert_data():
    try:
        request_data = request.get_json()

        if "data" not in request_data:
            return jsonify({"error": "Missing 'data' field in request"}), 400

        if insert_to_index(request_data["data"]):
            return jsonify({
  "message": "Data inserted successfully",
  "result": "Thank you very much for sharing your information with me.\nI believe it will help a lot of people."
}), 200
        else:
            return jsonify({"error": "Failed to insert data"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
