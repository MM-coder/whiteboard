# -*- coding: utf-8 -*-
from .app import app
from .config import load_config
import click
import sys


@click.command()
@click.argument('path', default='.', type=click.Path(exists=True,
                                                     file_okay=False,
                                                     writable=True))
@click.option('--port', default=5000)
@click.option('--host', default='127.0.0.1')
def run(path, port, host):
    app.config.update(load_config(path))
    app.config['NOTES_DIR'] = path
    click.launch('http://%s:%d/' % (host, port))
    app.run(host=host, port=port, use_reloader=False, use_debugger=False)
