import os

import flask
import requests

import runtime

def _source_url(repo_url, path):
    if not 'github.com' in repo_url:
        raise RuntimeError("Mountfile URLs must be Github URLs for now")
    if 'gist.github.com' in repo_url:
        gist_id = repo_url.split('/')[-1]
        return "https://gist.github.com/raw/{0}{1}".format(
                gist_id, path)
    elif 'github.com' in repo_url:
        base_url = repo_url.replace('github.com', 'raw.github.com')
        return "{0}/master{1}".format(base_url, path)

def _make_view(repo_url):
    def _view(path):
        source = requests.get(_source_url(repo_url, path))
        return runtime.run(flask.request, source.text)

if __name__ == "__main__":
    app = flask.Flask(__name__)

    with open('Mountfile', 'r') as mountfile:
        for mount in mountfile.readlines():
            mount_path, repo_url = mount.strip().split(':', 1)
            app.add_url_rule(
                "{0}<path:path>".format(mount_path),
                view_func=_make_view(repo_url.strip())) 

    app.run('0.0.0.0', int(os.environ.get("PORT", 5000)), debug=True)
