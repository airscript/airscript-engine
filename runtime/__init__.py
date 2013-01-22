import collections

import flask
import lupa

from runtime import base64
from runtime import json

__all__ = """
base64
json
""".split()

def _export_globals():
    d = dict()
    for k in __all__:
        d[k] = globals()[k]
    return d

def run(request, source):
    lua = lupa.LuaRuntime()

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
            body = json.dumps(value, cls=json.LuaEncoder)
            headers['Content-Type'] = 'application/json'
            body_set = True
        elif body_set and _is_mapping(value):
            for header in value:
                headers[header] = value[header]
    return flask.make_response(body, status, headers)

