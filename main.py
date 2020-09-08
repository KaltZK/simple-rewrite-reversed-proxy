from flask import Flask, request, abort
import toml
import requests
from collections import namedtuple
Config = namedtuple('Config', ('source', 'destination', 'port'))

def load_config() -> Config:
    with open('config.toml') as f:
        d = toml.load(f)
    return Config(**d)

config = load_config()

app = Flask(__name__)

def match_url(d):
    return config.destination.format(**d)


def pull_result(url):
    res = requests.get(url)
    return res.content

@app.route(config.source)
def _index(**d):
    target = match_url(d)
    if target is None:
        abort(404)
    return pull_result(target)


def main():
    app.run(host='0.0.0.0', port=config.port, debug=False)

if __name__ == "__main__":
    main()
