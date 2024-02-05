import asyncio
from concurrent import futures
import time
import traceback
from typing import Any, List
import grpc
import typer
from pydurable.cli.config import API_URL
from pydurable.cli.login import get_authenticated_session
import docker

from temporalio.api.workflowservice.v1.service_pb2_grpc import WorkflowServiceStub, add_WorkflowServiceServicer_to_server


TEMPORAL_URL = "3.215.127.194:7234"


app = typer.Typer()


@app.command('tctl')
def tctl(args: List[str]):
    session = get_authenticated_session()
    response = session.get(f'{API_URL}/apikey/').json()
    print(response)
    api_key = response[0]

    executor = futures.ThreadPoolExecutor()
    server = grpc.server(executor)
    
    executor.submit(run, server, api_key)

    client = docker.from_env()
    environment = {"TEMPORAL_CLI_ADDRESS": "localhost:7234"}
    
    try:
        container = client.containers.run(
            "temporalio/admin-tools:latest",
            command=args,
            entrypoint="/usr/local/bin/tctl",
            environment=environment,
            remove=True,
            network_mode="host",
        )

        print(container.decode("utf-8"))
    except docker.errors.ContainerError as e:
        print(f"Container execution failed with exit code {e.exit_status}")
        print("Container Output:")
        print(e.stderr.decode("utf-8"))
        
    server.stop(grace=True)


@app.command('ui')
def ui():
    session = get_authenticated_session()
    response = session.get(f'{API_URL}/apikey/').json()
    print(response)
    api_key = response[0]

    executor = futures.ThreadPoolExecutor()
    server = grpc.server(executor)
    
    executor.submit(run, server, api_key)

    client = docker.from_env()
    environment = {"TEMPORAL_ADDRESS": "localhost:7234",
                   "TEMPORAL_CORS_ORIGINS": "http://localhost:3000"}
    
    try:
        container = client.containers.run(
            "temporalio/ui:latest",
            environment=environment,
            remove=True,
            network_mode="host",
            detach=True
        )

        while True:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                print('Stopping')
                container.stop()
                break

    except docker.errors.ContainerError as e:
        print(f"Container execution failed with exit code {e.exit_status}")
        print("Container Output:")
        print(e.stderr.decode("utf-8"))
    
    print('Stopping server')
    server.stop(grace=True)


def run(server, api_key):
    channel = grpc.insecure_channel(TEMPORAL_URL)
    stub = WorkflowServiceStub(channel)
    
    servicer = ClientProxyServicer(stub, api_key)
    add_WorkflowServiceServicer_to_server(servicer, server)
    
    server.add_insecure_port('[::]:7234')
    server.start()


class ClientProxyServicer:
    def __init__(self, stub, api_key) -> None:
        self.stub = stub
        self.executor = futures.ThreadPoolExecutor(max_workers=100)
        self.api_key = api_key

    def __getattr__(self, __name: str) -> Any:
        def dynamic(request, context):
            try:
                print(f'{__name} request of type {type(request)}')
                stub_func = getattr(self.stub, __name)

                timeout = min(context.time_remaining(), 1000)
                response = stub_func(request, timeout=timeout, metadata=self.modify_metadata(context.invocation_metadata()))
                
                print(f'{__name} response of type {type(response)}.')
                return response
            except grpc.RpcError as e:
                print(f"{__name} failed with {type(e)} e: {traceback.format_exc()}")
                context.abort(e.code(), e.details())
            except Exception as e:
                print(f"{__name} failed with {type(e)} e: {traceback.format_exc()}")
                context.abort(grpc.StatusCode.UNKNOWN, str(e))
        return dynamic

    def modify_metadata(self, md):
        return (('durable_api_key', self.api_key),)
