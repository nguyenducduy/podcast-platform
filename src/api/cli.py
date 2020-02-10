import click
from flask import Flask

app = Flask(__name__)


@app.cli.command()
def initdb():
    """Initialize the database."""
    click.echo('Init the db')
