from flask import Flask, g, request, jsonify
import json
from auth import require_auth
from user_store import init_db, insert_login

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response


init_db()

@app.route('/api/save_user', methods=['POST', 'OPTIONS'])
@require_auth
def save_user():
    data = request.json or {}
    token_sub = g.auth.get('sub')
    submitted_sub = data.get('sub')
    email = data.get('email')
    name = data.get('name')
    raw_json = json.dumps(data, sort_keys=True)
    print(f"Received user data: sub={token_sub}, email={email}, name={name}")

    if submitted_sub and submitted_sub != token_sub:
        return jsonify({'error': 'Submitted sub does not match authenticated user'}), 403

    if not token_sub:
        return jsonify({'error': 'Missing authenticated sub'}), 400

    insert_login(token_sub, email, name, raw_json)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
