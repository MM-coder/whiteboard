from datetime import datetime
from flask import Flask, Response, request, redirect, abort, render_template, \
                  url_for, flash
from werkzeug.security import safe_join
import os
import sys
import re


app = Flask(__name__)
app.jinja_env.globals['today'] = datetime.today
app.secret_key = 'abc'


@app.route('/')
def home():
    files = []
    for fname in os.listdir(app.config['NOTES_DIR']):
        path = path_for(fname)
        if path is not None and not fname.startswith('.'):
            t = os.path.getmtime(path)
            with open(path) as f:
                files.append((fname, read_title(f), datetime.fromtimestamp(t)))
    files.sort(key=lambda x: x[2], reverse=True)
    return render_template('list.html', files=files)


@app.route('/', methods=['POST'])
def create():
    title = request.form.get('title', '')
    if not re.match(r'[A-Za-z0-9\'\s]+', title):
        flash('Invalid filename')
        return redirect(url_for('.home'), code=303)
    fname = title.lower().replace(' ', '-').replace('\'', '') + '.txt'
    path = path_for(fname, should_exist=False)
    if path is None:
        flash('That file exists')
        return redirect(url_for('.home'), code=303)
    with open(path, 'w') as f:
        write_note(f, title, '')
    return redirect(url_for('.edit', fname=fname), code=303)


@app.route('/<fname>', methods=['GET', 'PUT'])
def edit(fname):
    path = path_for(fname)
    if path is None:
        abort(404)

    if request.method == 'GET':
        title, text = read_note(fname)
        return render_template('edit.html', title=title, text=text)

    with open(path, 'w') as f:
        write_note(f, json_value('title'), json_value('text'))
    return Response(status=204)


def json_value(key):
    data = request.get_json()
    if data is None or not isinstance(data, dict):
        abort(400, 'Got %r for data' % data)
    elif key not in data or not isinstance(data[key], type(u'')):
        abort(400, '%s missing or bad type' % key)
    return data[key]


def path_for(fname, should_exist=True):
    path = safe_join(app.config['NOTES_DIR'], fname)
    if path is None or os.path.isfile(path) != should_exist:
        return None
    return path


def read_title(f):
    line = f.readline()
    if line.startswith('# ') and f.readline() == '\n':
        return line[2:-1]
    return None


def read_note(fname):
    with open(path_for(fname)) as f:
        return read_title(f), f.read()


def write_note(f, title, text):
    if title:
        f.write(u'# {0}\n\n'.format(title))
    f.write(text)


if __name__ == '__main__':
    app.config['NOTES_DIR'] = sys.argv[1]
    app.run(debug=True)
