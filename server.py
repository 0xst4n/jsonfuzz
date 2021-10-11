from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/login", methods=['POST'])
def login():
    content = request.json
    if 'username' in content and 'password' in content:
        username = content['username']
        password = content['password']
        if username == 'admin' and password == 'anus':
            return jsonify({'login': 'successful'}), 200
        else:
            return jsonify({'login': 'unsuccessful'}), 401

app.run()

# curl -i -X POST -H "Content-Type:application/json" -d "{\"username\": \"admin\",  \"password\" : \"Baggins\" }" http://localhost:5000/login