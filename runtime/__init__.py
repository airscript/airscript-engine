from __future__ import absolute_import

import collections

import flask
import json as json_
import lupa
import requests

from runtime import base64
from runtime import json

__all__ = """
base64
json
""".split()

try:
    lua = lupa.LuaRuntime()
except:
    pass # for local debugging without lupa

def _export_globals():
    d = dict()
    for k in __all__:
        d[k] = globals()[k]
    return d

def require(path):
    def _eval(source):
        try:
            module = lua.eval("""
function()
    {0}
end
""".format(source))
            return module()
        except Exception, e:
            raise e
            return {}
    webscript_lib = "https://raw.github.com/webscriptio/lib/master/{0}"
    builtin = requests.get(webscript_lib.format(path))
    if builtin.status_code == 200:
        return _eval(builtin.text)
    user, repo, path = path.split('/', 2)
    external_lib = "https://raw.github.com/{0}/{1}/master/{2}"
    external = requests.get(external_lib.format(user, repo, path))
    if external.status_code == 200:
        return _eval(external.text)
    raise RuntimeError( "unable to load lib")

def run(request, source):
    try:
        app = lua.eval("""
function(globals)
    for k,v in python.iterex(globals.items()) do
        _G[k] = v
    end
    {0}
end
""".format(source))
    except:
        return "Bad source", 400
    
    globals = _export_globals()
    globals['request'] = adapt_request(request)
    globals['require'] = require
    return adapt_response(
        app(lupa.as_attrgetter(globals)))

def adapt_request(request):
    """ builds a request object for lua from a flask request """
    def _default_table(input, filter=None):
        """ converts mapping to lua table w/o key errors """
        table = collections.defaultdict(lambda: False)
        for k,v in input.items():
            if filter is None:
                table[k] = v
            else:
                table[k] = filter(v)
        return table
    def _file_adaptor(file):
        return dict(
            type=file.content_type,
            filename=file.filename,
            content=file.stream.read())
    class adapted_request:
        form = _default_table(request.form)
        query = _default_table(request.args)
        querystring = request.query_string
        files = _default_table(request.files, _file_adaptor)
        body = request.data
        method = request.method
        remote_addr = request.remote_addr
        scheme = request.scheme
        port = 443 if request.is_secure else 80
        path = request.path
        headers = _default_table(request.headers)
    return adapted_request.__dict__


def adapt_response(response):
    """ builds a flask response from lua return value(s) """
    if not isinstance(response, tuple):
        response = (response,)
    status = 200
    headers = {"Content-Type": "text/plain"}
    body = ""
    body_set = False
    def _is_mapping(value):
        return isinstance(value, lupa._lupa._LuaTable) or \
                isinstance(value, dict)
    for value in response:
        if isinstance(value, basestring):
            body = value
            body_set = True
        elif isinstance(value, int):
            status = value
        elif not body_set and _is_mapping(value):
            body = json_.dumps(value, cls=json.LuaEncoder)
            headers['Content-Type'] = 'application/json'
            body_set = True
        elif body_set and _is_mapping(value):
            for header in value:
                headers[header] = value[header]
    return flask.make_response(body, status, headers)

