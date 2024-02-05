import asyncio
from dataclasses import asdict, is_dataclass
from typing import Any, Optional, Type, Union

from temporalio import activity, workflow
from temporalio.worker import (
    ActivityInboundInterceptor,
    ExecuteActivityInput,
    ExecuteWorkflowInput,
    Interceptor,
    WorkflowInboundInterceptor,
    WorkflowInterceptorClassInput,
)


class _ActivityInboundInterceptor(ActivityInboundInterceptor):
    async def execute_activity(self, input: ExecuteActivityInput) -> Any:
        activity_info = activity.info()
        print(f'Executing activity {activity_info}.')
        return await super().execute_activity(input)


class _WorkflowInterceptor(WorkflowInboundInterceptor):
    async def execute_workflow(self, input: ExecuteWorkflowInput) -> Any:
        workflow_info = workflow.info()
        print(f'Executing workflow {workflow_info}.')
        return await super().execute_workflow(input)


class MyInterceptor(Interceptor):
    def intercept_activity(self, next: ActivityInboundInterceptor) -> ActivityInboundInterceptor:
        return _ActivityInboundInterceptor(super().intercept_activity(next))

    def workflow_interceptor_class(self, input: WorkflowInterceptorClassInput) -> Optional[Type[WorkflowInboundInterceptor]]:
        return _WorkflowInterceptor
    
    async def wait(self):
        await asyncio.sleep(60 * 15)


# def has_tasks_in_queue(workflow_client, task_queue):
#     request = DescribeTaskQueueRequest(
#         namespace="default",
#         task_queue=TaskQueue(name=task_queue, kind=TaskQueueKind.TASK_QUEUE_KIND_NORMAL)
#     )
#     response = workflow_client.service_stub.DescribeTaskQueue(request)
#     return response.poller_info.possible_queries_count > 0
