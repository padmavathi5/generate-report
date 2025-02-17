from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/greet', methods=['GET'])
def greet():
    print("hello from code")

if __name__ == '__main__':
    app.run(debug=True)