from flask import Flask,\
    redirect

from models.cache import Cache
from models.api import require_apikey
import models.urlencoder

app = Flask(__name__)

@app.route('/')
def default():
    return "This is not the URL you're looking for."


@app.route('/<key>')
def get(key):
    url = Cache.get(key)
    if url:
        return redirect(url, code=301)
    else:
        return default()


@app.route('/put/<path:url>')
@require_apikey
def put(url):
    shortUrl = None
    try:
        newkey = Cache.get_next_key()
        print newkey
        encoder = models.urlencoder.UrlEncoder()
        shortUrl = encoder.encode_url(newkey)
        print shortUrl
        Cache.put(shortUrl, url)
    except BaseException as e:
        print e
    return "{0} {1}".format(url, shortUrl)


if __name__ == '__main__':
    app.run()
