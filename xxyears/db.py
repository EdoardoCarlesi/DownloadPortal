import sqlite3
import click
import os
from flask import current_app, g
import mysql.connector as mysql

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db_path = current_app.config['DATABASE']

    """
    if os.path.exists(db_path):
        reset = input("Database already exists. Do you want to reset it? [Y/n] ")
        
        if reset in ['Y']:
            click.echo('Database reset completed. Old database removed.')
            os.remove(db_path)
        else:
            click.echo('Database initialization cancelled. Database already exists.')
            exit()
    """

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Initialize the database or reset if it already exists."""
    init_db()
    click.echo('Database initialized.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


if __name__ == '__main__':
    init_db()
