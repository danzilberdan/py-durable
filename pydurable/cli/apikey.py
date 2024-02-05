import typer
from pydurable.cli.login import get_authenticated_session

from pydurable.cli.config import API_URL


app = typer.Typer()


@app.command('list')
def list_apikeys():
    session = get_authenticated_session()
    response = session.get(f'{API_URL}/apikey/')
    keys = response.json()
    if not keys:
        typer.echo('No API KEYS created yet.')
        return
    
    typer.echo(f'API KEYS:')
    for i, key in enumerate(keys):
        typer.echo(f' {i}. "{key}"')


@app.command('create')
def create_apikey():
    session = get_authenticated_session()
    res = session.post(f'{API_URL}/apikey/')
    key = res.json()
    typer.echo(f'Your new API KEY is: {key}.')


@app.command('delete')
def delete(index: int):
    session = get_authenticated_session()
    response = session.delete(f'{API_URL}/apikey/{index}')
    if not response.ok:
        typer.echo('Failed', response.json())
        return
    
    typer.echo(f'Deleted API KEY {index}.')
