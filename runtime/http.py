import requests

def request(T):
    res = requests.get(T['url'])
    return {
        'content': res.text, 
        'statuscode': res.status_code, 
        'headers': {}}

def load(path):
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
