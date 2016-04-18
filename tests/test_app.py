# -*- coding: utf-8 -*-
from click.testing import CliRunner
import datetime
import json
import pytest
import re
import webbrowser
import whiteboard.app
import whiteboard.cli


@pytest.fixture
def app():
    whiteboard.app.app.config['SECRET_KEY'] = 'Sekrit key!'
    whiteboard.app.app.config['DEBUG'] = True
    return whiteboard.app.app


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

        rv = client.post('/', data={'title': '../Test こんにちは'})
        assert rv.headers['Location'] == 'http://localhost/test.txt'
        assert rv.status_code == 303

        rv = client.get('/test.txt')
        assert u'value="../Test こんにちは"' in rv.data.decode('utf-8')
        assert rv.status_code == 200

        assert tmpdir.join('test.txt').read() == '# ../Test こんにちは\n\n'

        rv = client.post('/', data={'title': 'Test !!'})
        assert rv.headers['Location'] == 'http://localhost/test1.txt'
        assert rv.status_code == 303


def test_edit_file(app, tmpdir):
    app.config['NOTES_DIR'] = str(tmpdir)
    with app.test_client() as client:

        def assert_status(data, status):
            rv = client.put('/test-file.txt', data=json.dumps(data),
                            content_type='application/json')
            assert rv.status_code == status

        assert_status([], 404)

        f = tmpdir.join('test-file.txt')
        f.write('# Test File\n\n')

        assert_status(None, 400)
        assert_status([], 400)
        assert_status({'title': ''}, 400)
        assert_status({'text': ''}, 400)
        assert_status({'title': '', 'text': []}, 400)
        assert_status({'title': [], 'text': ''}, 400)

        assert_status({'title': '', 'text': ''}, 204)
        assert f.read() == ''

        assert_status({'title': 'こんにちは', 'text': ''}, 204)
        assert f.read() == '# こんにちは\n\n'

        assert_status({'title': '', 'text': 'キティ\n'}, 204)
        assert f.read() == 'キティ\n'

        assert_status({'title': 'こんにちは', 'text': 'キティ\n'}, 204)
        assert f.read() == '# こんにちは\n\nキティ\n'

        rv = client.get('/test-file.txt')
        html = rv.data.decode('utf-8')
        assert u'value="こんにちは"' in html
        assert u'>キティ\n</textarea>' in html


def test_cli(monkeypatch):
    monkeypatch.setattr('webbrowser.open', lambda x: None)
    runner = CliRunner()
    result = runner.invoke(whiteboard.cli.run, ['--host', 'fakehost'])
    assert result.exception
