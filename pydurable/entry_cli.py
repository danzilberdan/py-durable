import typer
from pydurable.cli.login import login
from pydurable.cli.apikey import app as apikey
from pydurable.cli.aws import app as aws
from pydurable.cli.func import app as func
from pydurable.cli.temporal import app as temporal


LOGIN_PORT = 54987
CLIENT_ID = '685954567384-9otb323plmau5iutge14kb4l7aei889n.apps.googleusercontent.com'
API = 'http://localhost:8000'


app = typer.Typer()
app.command()(login)
app.add_typer(apikey, name='keys')
app.add_typer(aws, name='aws')
app.add_typer(func, name='func')
app.add_typer(temporal, name='temporal')


def main():
    app()
    

if __name__ == '__main__':
    app()
