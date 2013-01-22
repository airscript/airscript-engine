import requests

def request(T):
    res = requests.get(T['url'])
    return {
        'content': res.text, 
        'statuscode': res.status_code, 
        'headers': {}}
