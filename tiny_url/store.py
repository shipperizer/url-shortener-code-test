from uuid import uuid4
from urllib.parse import urlparse

from flask import url_for
from werkzeug import exceptions

from tiny_url.exceptions import RequestError, ResourceExists
from tiny_url.db import db, db_commit, Url


def get_url(uuid=None, url=None, tiny_url=None):
    if uuid:
        return Url.query.get_or_404(uuid)
    elif url:
        return Url.query.filter_by(url=_check_url(url)).first_or_404()
    else:
        raise RequestError


def get_urls(page=1, pagination=False):
    if pagination:
        return Url.query.paginate(page, 20, False)
    else:
        return Url.query.all()


def create_tiny_url(url):
    try:
        get_url(url=url)
        raise ResourceExists
    except exceptions.NotFound:
        u = Url(uuid=str(uuid4()), url=_check_url(url))
        u.tiny_url = url_for('api.get_tiny', tiny_url=u.uuid, _external=True)
        db.session.add(u)
        db_commit()
        return u


def _check_url(url):
    if not (url.startswith('http') or url.startswith('https')):
        url = 'http://' + url
    return urlparse(url).geturl()
