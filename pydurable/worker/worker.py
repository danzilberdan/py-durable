from temporalio.worker import Worker

from pydurable.worker.client import get_client
from pydurable.worker.wait_for_exit import wait_for_exit


async def run(workflows, activities, api_key: str=None, context=None, function_name=None):
    if not function_name and context:
        function_name = context.function_name

    if not function_name:
        raise KeyError('Run function called without AWS Lambda context or a function name. Please provide one.')

    client = await get_client(api_key)

    async with Worker(
        client,
        task_queue=function_name,
        workflows=workflows,
        activities=activities,
        max_concurrent_activity_task_polls=1,
        max_concurrent_workflow_task_polls=1,
    ):
       print('Started Worker')
       await wait_for_exit(client, function_name)

    return {"statusCode": 200, "body": "Completed"}
