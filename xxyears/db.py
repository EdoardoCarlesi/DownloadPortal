import sqlite3
import click
from flask import current_app, g
import mysql.connector as mysql

def remote_db_connect():

    HOST = "sql11.freemysqlhosting.net"
    DATABASE = "sql11697861"
    USER = "sql11697861"
    PASSWORD = "2TGfCHmHYu"

    db_connection = mysql.connect(host=HOST, 
                                  database=DATABASE, 
                                  user=USER, 
                                  password=PASSWORD)

    print("Connected to:", db_connection.get_server_info())

    cursor = db_connection.cursor()
    # get database information
    cursor.execute("select database();")
    database_name = cursor.fetchone()
    print("[+] You are connected to the database:", database_name)

    cursor.execute(f"create database if not exists {DATABASE}")

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

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


if __name__ == '__main__':

    remote_db_connect()
