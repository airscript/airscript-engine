import os
from flask import Flask, request, make_response
app = Flask(__name__)

import lupa
import requests
import collections
import json

import runtime

@app.route("/<path:path>")
def run(path):
    source = requests.get("https://gist.github.com/raw/{0}".format(path))
    return runtime.run(request, source.text)

if __name__ == "__main__":
    app.run('0.0.0.0', int(os.environ.get("PORT", 5000)), debug=True)
