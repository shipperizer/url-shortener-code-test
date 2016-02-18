from unittest.mock import patch, MagicMock
from copy import deepcopy

import pytest
from webtest import TestApp

from tiny_url.app import create_app
from tiny_url.db import Url


URL_JSON = {
    'url': 'http://www.google.com',
    'tiny_url': 'http://localhost:5000/tiny/aaf7742b-3779-47a9-b119-6ef855d743e7',
    'uuid': 'aaf7742b-3779-47a9-b119-6ef855d743e7'
}


@pytest.fixture
def application():
    app = create_app()
    test_app = TestApp(app)
    return test_app


@patch('tiny_url.blueprints.api.store')
def test_url_list(store, application):
    store.get_urls.return_value = MagicMock(items=[Url.deserialize(URL_JSON)])
    response = application.get('/url')
    store.get_urls.assert_called_with(page=1, pagination=True)
    assert response.status_code == 200
    body = response.json
    assert 'urls' in body
    assert 'url' in body['urls'][0].keys()
    assert 'tiny_url' in body['urls'][0].keys()
    assert 'uuid' in body['urls'][0].keys()


@patch('tiny_url.blueprints.api.store')
def test_url_detail(store, application):
    store.get_url.return_value = Url.deserialize(URL_JSON)
    response = application.get('/url', params={'url': URL_JSON['url']})
    store.get_url.assert_called_with(url=URL_JSON['url'])
    assert response.status_code == 200
    body = response.json
    assert 'url' in body
    assert 'tiny_url' in body
    assert 'uuid' in body


@patch('tiny_url.blueprints.api.store')
def test_tiny_url_detail(store, application):
    store.get_url.return_value = Url.deserialize(URL_JSON)
    response = application.get('/tiny/aaf7742b-3779-47a9-b119-6ef855d743e7')
    store.get_url.assert_called_with(uuid='aaf7742b-3779-47a9-b119-6ef855d743e7')
    assert response.status_code == 302
    assert URL_JSON['url'] == response.location


@patch('tiny_url.blueprints.api.store')
def test_create_tiny_url(store, application):
    store.create_tiny_url.return_value = Url.deserialize(URL_JSON)
    response = application.post_json('/tiny', params={'url': URL_JSON['url']})
    store.create_tiny_url.assert_called_with(URL_JSON['url'])
    assert response.status_code == 200
    body = response.json
    assert 'tiny_url' in body
    assert body['tiny_url'] == URL_JSON['tiny_url']
