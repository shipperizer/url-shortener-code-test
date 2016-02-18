from flask import Blueprint, request, jsonify, render_template, redirect

from tiny_url import store


api = Blueprint('api', __name__)


@api.route('/url', methods=['GET'])
def get_url():
    param_url = request.args.get('url')
    page = request.args.get('page', 1)
    if param_url:
        url = store.get_url(url=param_url)
        return jsonify(url.serialize())
    else:
        urls = store.get_urls(page=page, pagination=True)
        return jsonify(urls=[url.serialize() for url in urls.items])


@api.route('/tiny/<tiny_url>', methods=['GET'])
def get_tiny(tiny_url):
    url = store.get_url(uuid=tiny_url)
    return redirect(url.url, code=302)


@api.route('/tiny', methods=['POST'])
def create_tiny_url():
    json_url = request.get_json(force=True)
    url = store.create_tiny_url(json_url['url'])
    return jsonify(tiny_url=url.tiny_url)


@api.route('/tiny', methods=['GET'])
def url_view():
    return render_template('url.html')
