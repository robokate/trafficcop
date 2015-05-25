from urllib import quote_plus
import json

from flask import Flask,\
    redirect,\
    request,\
    render_template
from flask_bootstrap import Bootstrap

from models.cache import Cache
from models.api import require_apikey
from models.shortenform import ShortenForm

app = Flask(__name__)
Bootstrap(app)

@app.route('/', defaults={'key': None})
@app.route('/<key>')
def default(key):
    try:
        if key is not None:
            url = Cache.get(key)
            if url:
                print url
                return redirect(url, code=301)
        try:
            return render_template('index.html')
        except BaseException as e:
            print e
    except BaseException as e:
        print e


@app.route('/shorten', methods=['GET', 'POST'])
@require_apikey
def put_via_form():
    form = ShortenForm(request.form)
    if request.method == 'POST' and form.validate():
        url = form.url_to_shorten.data
        short_url = None
        try:
            short_url = Cache.put_url(url)
        except BaseException as e:
            print e
        return render_template('shorten_success.html', url=url, short_url=short_url)
    return render_template('shorten.html', form=form, apikey=request.args.get('apikey'))


@app.route('/shorten/<path:url>', methods=['POST'])
@require_apikey
def put_via_service(url):
    short_url = None
    try:
        short_url = Cache.put_url(url)
    except BaseException as e:
        print e
    results = json.dumps({'short_url': short_url, 'long_url': url})
    return str(results)


if __name__ == '__main__':
    app.run()
