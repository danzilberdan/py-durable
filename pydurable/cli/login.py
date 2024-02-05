import datetime
import json
import logging
from pathlib import Path
import threading
from typing import Any
import requests
import typer
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from pydurable.cli.config import API_URL


LOGIN_PORT = 54987
CLIENT_ID = '685954567384-9otb323plmau5iutge14kb4l7aei889n.apps.googleusercontent.com'


def login():
    code = None

    class RedirectHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            nonlocal code
            try:
                code = query_params['code'][0]
            except KeyError:
                pass
            self.send_response(200)
            self.send_header("Content-type", "text/text")
            self.end_headers()
            response_message = "Logged In to Durable"
            self.wfile.write(response_message.encode('utf-8'))
            if code:
                threading.Thread(target=self.server.shutdown).start()
        
        def log_message(self, format: str, *args: Any) -> None:
            pass

    logging.getLogger('http.server').setLevel(logging.WARNING)
    httpd = HTTPServer(("127.0.0.1", LOGIN_PORT), RedirectHandler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.start()
    try:
        typer.launch('https://accounts.google.com/o/oauth2/v2/auth?response_type=code&scope=https://www.googleapis.com/auth/userinfo.email'
                     f'&client_id={CLIENT_ID}&redirect_uri=http://127.0.0.1:{LOGIN_PORT}')
        server_thread.join()
        print("Logged In")
    except KeyboardInterrupt:
        print("Stopping.")
    else:
        httpd.shutdown()

    tokens = requests.get(f"{API_URL}/login/google", params={
        "code": code
    }).json()
    save_tokens(tokens)


DURABLE_DIR = Path.home() / ".durable"
TOKEN_PATH = DURABLE_DIR / "token"


def save_tokens(tokens):
    DURABLE_DIR.mkdir(parents=True, exist_ok=True)
    with TOKEN_PATH.open(mode='w') as token_file:
        json.dump(tokens, token_file)


def get_tokens():
    with TOKEN_PATH.open(mode='r') as token_file:
        return json.load(token_file)


def get_authenticated_session():
    tokens = get_tokens()
    session = requests.Session()
    session.headers.update({'Authorization': f'Bearer {tokens["access_token"]}'})
    return session
