from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/login", methods=['POST'])
def login():
    content = request.json
    if 'username' in content and 'password' in content:
        username = content['username']
        password = content['password']
        if (username == 'admin' and password == 'uranus') or (username == 'admin' and password == 'nicole'):
            return jsonify({'login': 'SUCCESFUL!'}), 200
        else:
            return jsonify({'login': 'unsuccessful :('}), 401

app.run()