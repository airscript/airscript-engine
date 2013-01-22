import os
from flask import Flask, request
app = Flask(__name__)

import requests

import runtime

@app.route("/<path:path>")
def run(path):
    source = requests.get("https://gist.github.com/raw/{0}".format(path))
    return runtime.run(request, source.text)

if __name__ == "__main__":
    app.run('0.0.0.0', int(os.environ.get("PORT", 5000)), debug=True)
