from flask import Flask, Response, request, abort, render_template
from werkzeug.security import safe_join
import os

app = Flask(__name__)


@app.route('/<int:id>', methods=['GET', 'PUT'])
def note(id):
    if not path_for(id):
        abort(404)

    if request.method == 'GET':
        title, text = readNote(id)
        return render_template('edit.html', title=title, text=text)

    data = request.get_json()
    if data is None or not isinstance(data, dict):
        abort(400, 'Got %r for data' % data)
    for k in ('title', 'text'):
        if k not in data or not isinstance(data[k], type(u'')):
            abort(400, '%s missing or bad type' % k)

    writeNote(id, data['title'], data['text'])
    return Response(status=204)


def path_for(id):
    path = safe_join('notes', str(id))
    if path is None or not os.path.isfile(path):
        return None
    return path


def readNote(id):
    with open(path_for(id)) as f:
        line = f.readline()
        assert line.startswith('# ')
        title = line[2:].strip()
        assert f.readline() == '\n'
        return title, f.read()


def writeNote(id, title, text):
    with open(path_for(id), 'w') as f:
        f.write(u'# {0}\n\n'.format(title))
        f.write(text)


if __name__ == '__main__':
    app.run(debug=True)
