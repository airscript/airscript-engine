import requests

def request(T):
    res = requests.request(
            url=T['url'],
            method=T.get('method', 'GET'),
            params=T.get('params'),
            data=T.get('data'),
            headers=T.get('headers'),
            auth=T.get('auth'))
    return {
        'content': res.text, 
        'statuscode': res.status_code, 
        'headers': res.headers}

def load(path):
    if path.endswith('.lua'):
        path = path[:-4]
    webscript_lib = "https://raw.github.com/webscriptio/lib/master/{0}.lua"
    builtin = requests.get(webscript_lib.format(path))
    if builtin.status_code == 200:
        return builtin.text
    user, repo, path = path.split('/', 2)
    external_lib = "https://raw.github.com/{0}/{1}/master/{2}.lua"
    external = requests.get(external_lib.format(user, repo, path))
    if external.status_code == 200:
        return external.text
    return ""
