import json

from flask import Flask, request

import intents

app = Flask(__name__)

def auth_check(req):
    with open('auth.json') as f:
        return req.headers.get('Authorization') in json.loads(f.read())['private/approved-keys']


@app.route('/', methods=['GET', 'POST'])
def main():
    response = str(intents.get_response(request.get_json()))
    return response

