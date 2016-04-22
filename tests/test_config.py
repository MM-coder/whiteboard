# -*- coding: utf-8 -*-
from whiteboard.config import load_config, DEFAULT_CONFIG
import pytest


@pytest.fixture
def temp_home(tmpdir, monkeypatch):
    f = tmpdir.join('.whiteboardrc_global')
    monkeypatch.setattr('whiteboard.config.GLOBAL_CONFIG_PATH', str(f))
    return f


def test_default_config(temp_home):
    assert load_config('.') == DEFAULT_CONFIG


def test_global_config(temp_home, tmpdir, bad_json):
    temp_home.write('{"test": 1}')
    data = load_config(str(tmpdir))
    assert data['test'] == 1
    assert 'SECRET_KEY' in data


def test_local_override(temp_home, tmpdir, bad_json):
    temp_home.write('{"a": 1, "b": 2}')
    tmpdir.join('.whiteboardrc').write(u'{"b": "こんにちは"}')
    data = load_config(str(tmpdir))
    assert data['a'] == 1
    assert data['b'] == u'こんにちは'
    assert 'SECRET_KEY' in data


@pytest.fixture
def bad_json(capsys):
    """Return a function to get the error message, with assertions."""
    def inner(path):
        with pytest.raises(SystemExit) as e:
            load_config(path)
        out, err = capsys.readouterr()
        assert out == ''
        return err
    return inner


def test_bad_local_json(temp_home, tmpdir, bad_json):
    tmpdir.join('.whiteboardrc').write('{{{}}}')
    assert bad_json(str(tmpdir)) != ''


def test_bad_global_json(temp_home, tmpdir, bad_json):
    temp_home.write('{{{}}}')
    assert bad_json(str(tmpdir)) != ''


def test_non_dict_json(temp_home, tmpdir, bad_json):
    temp_home.write('[]')
    msg = bad_json(str(tmpdir))
    assert 'Expecting config to be dict, got list' in msg
