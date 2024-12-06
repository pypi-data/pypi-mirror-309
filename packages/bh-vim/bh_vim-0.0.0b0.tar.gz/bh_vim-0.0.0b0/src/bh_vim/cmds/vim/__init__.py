import os

import typer

app = typer.Typer()

@app.command()
def foo():
    print('the foo')

@app.command()
def bar():
    print('the bar')
