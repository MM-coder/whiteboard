# -*- coding: utf-8 -*-
from click.testing import CliRunner
import datetime
import json
import pytest
import re
import whiteboard.app
import whiteboard.cli


@pytest.fixture
def app():
    whiteboard.app.app.config['SECRET_KEY'] = 'Sekrit key!'
    return whiteboard.app.app


def json_put(client, url, data, status=None, msg=None):
    rv = client.put(url, data=json.dumps(data),
                    content_type='application/json')
    if status is not None:
        assert rv.status_code == status
    return rv


def test_empty_list(app, tmpdir):
    app.config['NOTES_DIR'] = str(tmpdir)
    with app.test_client() as client:
        rv = client.get('/')
        assert b'<div class="listing">' not in rv.data
        assert rv.status_code == 200


def test_file_list(app, tmpdir):
    app.config['NOTES_DIR'] = str(tmpdir)
    with app.test_client() as client:
        test1 = tmpdir.join('test1.txt')
        test1.open('a').close()
        test1.setmtime(1356048000)  # Dec 21, 2012
        tmpdir.join('test2.txt').write('# Hello\n\n')

        rv = client.get('/')
        assert (b'<a href="/test1.txt" class="listing-title">'
                b'Untitled</a>') in rv.data
        assert (b'<a href="/test2.txt" class="listing-title">'
                b'Hello</a>') in rv.data
        assert rv.data.index(b'Hello') < rv.data.index(b'Untitled')
        assert rv.status_code == 200


def test_create_file(app, tmpdir):
    app.config['NOTES_DIR'] = str(tmpdir)
    with app.test_client() as client:
        rv = client.get('/test-file.txt')
        assert rv.status_code == 404

        rv = client.post('/', data={'title': 'Test File'})
        assert rv.headers['Location'] == 'http://localhost/test-file.txt'
        assert rv.status_code == 303

        rv = client.get('/test-file.txt')
        assert b'value="Test File"' in rv.data
        assert rv.status_code == 200

        assert tmpdir.join('test-file.txt').read() == '# Test File\n\n'

        rv = client.post('/', data={'title': 'Test File'})
        assert rv.headers['Location'] == 'http://localhost/'
        assert rv.status_code == 303


def test_edit_file(app, tmpdir):
    app.config['NOTES_DIR'] = str(tmpdir)
    with app.test_client() as client:

        json_put(client, '/test-file.txt', [], 404)

        f = tmpdir.join('test-file.txt')
        f.write('# Test File\n\n')

        json_put(client, '/test-file.txt', None, 400)
        json_put(client, '/test-file.txt', [], 400)
        json_put(client, '/test-file.txt', {'title': ''}, 400)
        json_put(client, '/test-file.txt', {'text': ''}, 400)
        json_put(client, '/test-file.txt', {'title': '', 'text': []}, 400)
        json_put(client, '/test-file.txt', {'title': [], 'text': ''}, 400)

        json_put(client, '/test-file.txt', {'title': '', 'text': ''}, 204)
        assert f.read() == ''

        json_put(client, '/test-file.txt', {'title': '', 'text': 'Abc'}, 204)
        assert f.read() == 'Abc'

        json_put(client, '/test-file.txt', {'title': 'Hi', 'text': 'Abc'}, 204)
        assert f.read() == '# Hi\n\nAbc'


def test_cli():
    runner = CliRunner()
    result = runner.invoke(whiteboard.cli.run, ['--host', 'fakehost'])
    assert result.exception
