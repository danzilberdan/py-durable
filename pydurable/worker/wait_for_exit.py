import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
import traceback
from typing import Dict, List
from temporalio.client import Client
from temporalio.api.workflowservice.v1 import (
    GetWorkflowExecutionHistoryReverseRequest,
    GetWorkflowExecutionHistoryReverseResponse,
    ListOpenWorkflowExecutionsRequest,
    ListOpenWorkflowExecutionsResponse
)
from temporalio.api.common.v1 import WorkflowExecution
from temporalio.api.history.v1 import History
from temporalio.api.enums.v1 import HistoryEventFilterType, EventType
from temporalio.api.workflow.v1 import WorkflowExecutionInfo


@dataclass(frozen=True)
class VersionData:
    version: str
    updated: datetime


async def wait_for_exit(client: Client, task_queue):
    versions = {}
    errors = 0

    while True:
        try:
            if await should_stop(client, task_queue, versions):
                print('Exiting')
                return
            
            print('Not Exiting')
        except Exception as e:
            print(f'Error while checking for stopping condition {traceback.format_exc()} Exiting.')
            errors += 1
            if errors >= 5:
                break
        await asyncio.sleep(1)


async def should_stop(client, task_queue, versions: Dict[str, VersionData]):
    namespace = client.config()['namespace']
    open_wf_response: ListOpenWorkflowExecutionsResponse = \
        await client.service_client.workflow_service.list_open_workflow_executions(
            ListOpenWorkflowExecutionsRequest(
                namespace=namespace
            )
        )
    
    executions_info: List[WorkflowExecutionInfo] = \
        filter(lambda execinfo: execinfo.task_queue == task_queue, open_wf_response.executions)
    
    for execution_info in executions_info:
        wf_history_response: GetWorkflowExecutionHistoryReverseResponse = \
            await client.service_client.workflow_service.get_workflow_execution_history_reverse(
                GetWorkflowExecutionHistoryReverseRequest(
                    namespace=namespace,
                    execution=WorkflowExecution(workflow_id=execution_info.execution.workflow_id),
                    maximum_page_size=1
                )
            )
        
        history: History = wf_history_response.history
        if len(history.events) == 0:
            continue

        last_event = history.events[0]
        if last_event.event_type == EventType.EVENT_TYPE_TIMER_STARTED:
            event_time = last_event.event_time.ToDatetime()
            timer_seconds = last_event.timer_started_event_attributes.start_to_fire_timeout.ToTimedelta()
            end_time = event_time + timer_seconds
            now = datetime.now()
            if (end_time - now).total_seconds() > 10:
                continue

        if not execution_info.execution.run_id in versions:
            versions[execution_info.execution.run_id] = VersionData(version=last_event.event_id, updated=datetime.now())

        old_version = versions[execution_info.execution.run_id]

        if old_version.version != last_event.event_id:
            versions[execution_info.execution.run_id] = VersionData(version=last_event.event_id, updated=datetime.now())
        elif (datetime.now() - old_version.updated).total_seconds() > 10:
            print(f'run_id {execution_info.execution.run_id} stuck on event {last_event.event_id} for too long.')
            continue

        return False

    return True
