import typer
from pydurable.cli.config import API_URL
from pydurable.cli.login import get_authenticated_session


app = typer.Typer()


@app.command('info')
def info():
    session = get_authenticated_session()
    data = session.get(f'{API_URL}/aws/info').json()
    typer.echo(data)


@app.command('update-role')
def update_role(role: str):
    session = get_authenticated_session()
    response = session.put(f'{API_URL}/aws/role/{role}').json()
    typer.echo(response)


@app.command('update-account')
def update_account(account_id: str):
    session = get_authenticated_session()
    response = session.put(f'{API_URL}/aws/account/{account_id}').json()
    typer.echo(response)
