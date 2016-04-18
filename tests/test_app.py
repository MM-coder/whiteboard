# -*- coding: utf-8 -*-
import pytest
import whiteboard.app


@pytest.fixture
def app(tmpdir):
    whiteboard.app.app.config['NOTES_DIR'] = str(tmpdir)
    whiteboard.app.app.config['SECRET_KEY'] = 'Sekrit key!'
    return whiteboard.app.app


def test_empty_list(app):
    with app.test_client() as client:
        rv = client.get('/')
        assert b'<div class="listing">' not in rv.data
        assert rv.status_code == 200
