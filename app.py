from datetime import datetime
from flask import Flask, Response, request, abort, render_template
from werkzeug.security import safe_join
import os
import sys

app = Flask(__name__)


@app.route('/')
def home():
    files = []
    for fname in os.listdir(app.config['NOTES_DIR']):
        path = path_for(fname)
        if path is not None and not fname.startswith('.'):
            t = os.path.getmtime(path)
            with open(path) as f:
                files.append((fname, read_title(f), datetime.fromtimestamp(t)))
    return render_template('list.html', files=files)


@app.route('/<fname>', methods=['GET', 'PUT'])
def edit(fname):
    if not path_for(fname):
        abort(404)

    if request.method == 'GET':
        title, text = read_note(fname)
        return render_template('edit.html', title=title, text=text)

    data = request.get_json()
    if data is None or not isinstance(data, dict):
        abort(400, 'Got %r for data' % data)
    for k in ('title', 'text'):
        if k not in data or not isinstance(data[k], type(u'')):
            abort(400, '%s missing or bad type' % k)

    write_note(fname, data['title'], data['text'])
    return Response(status=204)


def path_for(fname):
    path = safe_join(app.config['NOTES_DIR'], fname)
    if path is None or not os.path.isfile(path):
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


def write_note(fname, title, text):
    with open(path_for(fname), 'w') as f:
        f.write(u'# {0}\n\n'.format(title))
        f.write(text)


if __name__ == '__main__':
    app.config['NOTES_DIR'] = sys.argv[1]
    app.run(debug=True)
