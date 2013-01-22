import os
from flask import Flask, request, make_response
app = Flask(__name__)

import lupa
import requests
import collections
import json

@app.route("/<path:path>")
def hello(path):
    lua = lupa.LuaRuntime()
    src = requests.get("https://gist.github.com/raw/{0}".format(path))
    app = lua.eval("""
function(request)
    {0}
end
""".format(src.text))
    query = collections.defaultdict(lambda: False)
    for k,v in request.args.items():
        query[k] = v
    req = dict(
        query=query
    )
    return build_response(app(req))

def build_response(resp):
    if not isinstance(resp, list):
        resp = [resp]
    status = 200
    headers = {"Content-Type": "text/plain"}
    body = ""
    body_set = False
    for value in resp:
        if isinstance(value, str):
            body = value
            body_set = True
        elif isinstance(value, int):
            status = value
        elif not body_set and isinstance(value, dict):
            body = json.dumps(value)
            headers['Content-Type'] = 'application/json'
            body_set = True
        elif body_set and isinstance(value, dict):
            for header in value:
                headers[header] = value[header]
    response = make_response(body, status)
    for header in headers:
        response.headers[header] = headers[header]
    return response

if __name__ == "__main__":
    app.run('0.0.0.0', int(os.environ.get("PORT", 5000)), debug=True)
