# -*- coding: utf-8 -*-
"""Abstraction of notes on the filesystem."""
from datetime import datetime
from flask import current_app
from werkzeug.security import safe_join
import os


class Note(object):

    def __init__(self, filename, title, text=None, mtime=None):
        self.filename = filename
        self.title = title
        self.text = text
        self.mtime = mtime


def _path_for(fname):
    path = safe_join(current_app.config['NOTES_DIR'], fname)
    return path


def note_exists(fname):
    path = _path_for(fname)
    return (not fname.startswith('.') and os.path.exists(path) and
            os.path.isfile(path))


def _read_title(f):
    line = f.readline()
    if line.startswith(b'# ') and f.readline() == b'\n':
        return line[2:-1].decode('utf-8')
    return None


def read_note(fname):
    """Assumes filename is valid."""
    with open(_path_for(fname), 'rb') as f:
        return Note(fname, _read_title(f), f.read().decode('utf-8'))


def write_note(note):
    """Assumes filename is valid."""
    with open(_path_for(note.filename), 'wb') as f:
        if note.title:
            f.write(b'# ')
            f.write(note.title.encode('utf-8'))
            f.write(b'\n\n')
        if note.text:
            f.write(note.text.encode('utf-8'))


def list_notes():
    notes = []
    for fname in os.listdir(current_app.config['NOTES_DIR']):
        if note_exists(fname):
            path = _path_for(fname)
            ts = os.path.getmtime(path)
            with open(path, 'rb') as f:
                title = _read_title(f)
                note = Note(fname, title, None, datetime.fromtimestamp(ts))
                notes.append(note)
    notes.sort(key=lambda x: x.mtime, reverse=True)
    return notes
