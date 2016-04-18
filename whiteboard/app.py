# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, Response, request, redirect, abort, render_template, \
                  url_for, flash
from .notes import Note, note_exists, read_note, write_note, list_notes
import re


app = Flask(__name__)
app.jinja_env.globals['today'] = datetime.today


@app.route('/')
def list():
    notes = list_notes()
    return render_template('list.html', notes=notes)


@app.route('/', methods=['POST'])
def create():
    title = request.form.get('title', u'')
    prefix = (re.sub(u'[^A-Za-z0-9\s]', u'', title).strip().lower()
              .replace(u' ', u'-'))
    fname = prefix + u'.txt'
    n = 1
    while note_exists(fname):
        fname = u'%s%d.txt' % (prefix, n)
        n += 1
    note = Note(fname, title, None)
    write_note(note)
    return redirect(url_for('.edit', fname=note.filename), code=303)


@app.route('/<fname>')
def edit(fname):
    if not note_exists(fname):
        abort(404)
    note = read_note(fname)
    return render_template('edit.html', note=note)


@app.route('/<fname>', methods=['PUT'])
def save(fname):
    if not note_exists(fname):
        abort(404)
    note = Note(fname, json_value('title'), json_value('text'))
    write_note(note)
    return Response(status=204)


def json_value(key):
    data = request.get_json()
    if data is None or not isinstance(data, dict):
        abort(400, 'Got %r for data' % data)
    elif key not in data or not isinstance(data[key], type(u'')):
        abort(400, '%s missing or bad type' % key)
    return data[key]
