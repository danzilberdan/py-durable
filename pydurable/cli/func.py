import typer
from pydurable.cli.config import API_URL
from pydurable.cli.login import get_authenticated_session


app = typer.Typer()


@app.command('register')
def register_func(name: str):
    session = get_authenticated_session()
    response = session.post(f'{API_URL}/func/register/{name}').json()
    typer.echo(response)


@app.command('list')
def list_funcs():
    session = get_authenticated_session()
    funcs = session.get(f'{API_URL}/func/').json()
    for i, func in enumerate(funcs):
        typer.echo(f'{i}. "{func}"')


@app.command('delete')
def delete_func(name: str):
    session = get_authenticated_session()
    response = session.delete(f'{API_URL}/func/{name}').json()
    typer.echo(response)
