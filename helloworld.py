import os
from flask import Flask, request, make_response
app = Flask(__name__)

import lupa
import requests
import collections
import json

import runtime

class LuaEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, lupa._lupa._LuaTable):
            return dict(obj)
        return json.JSONEncoder.default(self, obj)

@app.route("/<path:path>")
def hello(path):
    lua = lupa.LuaRuntime()
    src = requests.get("https://gist.github.com/raw/{0}".format(path))
    try:
        app = lua.eval("""
function(globals)
    for k,v in python.iterex(globals.items()) do
        _G[k] = v
    end
    {0}
end
""".format(src.text))
    except:
        return "Bad source", 400
    globals = dict(
            request=build_request(request),)
    globals.update(runtime._export())
    output = app(lupa.as_attrgetter(globals))
    print output
    return build_response(output)

def build_request(request):
    def _default_table(input, filter=None):
        table = collections.defaultdict(lambda: False)
        for k,v in input.items():
            if filter is None:
                table[k] = v
            else:
                table[k] = filter(v)
        return table
    def _file(file):
        return dict(
            type=file.content_type,
            filename=file.filename,
            content=file.stream.read())
    class _req:
        form = _default_table(request.form)
        query = _default_table(request.args)
        querystring = request.query_string
        files = _default_table(request.files, _file)
        body = request.data
        method = request.method
        remote_addr = request.remote_addr
        scheme = request.scheme
        port = 443 if request.is_secure else 80
        path = request.path
        headers = _default_table(request.headers)
    return _req.__dict__


def build_response(resp):
    if not isinstance(resp, tuple):
        resp = (resp,)
    status = 200
    headers = {"Content-Type": "text/plain"}
    body = ""
    body_set = False
    def is_mapping(value):
        return isinstance(value, lupa._lupa._LuaTable) or isinstance(value, dict)
    for value in resp:
        if isinstance(value, basestring):
            body = value
            body_set = True
        elif isinstance(value, int):
            status = value
        elif not body_set and is_mapping(value):
            body = json.dumps(value, cls=LuaEncoder)
            headers['Content-Type'] = 'application/json'
            body_set = True
        elif body_set and is_mapping(value):
            for header in value:
                headers[header] = value[header]
    return make_response(body, status, headers)

if __name__ == "__main__":
    app.run('0.0.0.0', int(os.environ.get("PORT", 5000)), debug=True)
