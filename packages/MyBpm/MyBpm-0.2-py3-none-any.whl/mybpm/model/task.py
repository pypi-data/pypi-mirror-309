import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, ForwardRef, List, Optional, Union

from pydantic import BaseModel, Field, root_validator
from mybpm.camunda import hisprocessinst, hisvariableinst
from mybpm.constant import (
    PROCESS_STATUS,
    TASK_STATUS,
    URL_CAMUNDA_ENGINE,
    ApprovalTaskStatus,
    BpmDeleteReason,
    BpmInstanceStatus,
)
from mybpm.service import process_variables
from mybpm.utils import util


def pack_task_status(task_id):
    getlist = hisvariableinst.GetVariables(url=URL_CAMUNDA_ENGINE, variable_name=TASK_STATUS, task_id_in=task_id)
    variables = getlist()
    if variables is None or len(variables) == 0:
        return ApprovalTaskStatus.PENDING.value
    return variables[0].value


class ProcessTask(BaseModel):
    id: str = None
    task_id: str = None
    task_name: str = None
    instance_id: str = None
    definition_id: str = None
    definition_key: str = None
    task_status: str = None
    creator: str = None
    task_assignee: str = None
    node_id: str = None
    node_name: str = None
    create_time: int = None
    update_time: int = None
    end_time: int = 0
    delete_reason: str = None

    @classmethod
    def packTask(cls, task_):
        if task_ is None:
            return None

        process_task = ProcessTask(
            id=task_.id_,
            task_id=task_.id_,
            task_name=task_.name,
            instance_id=task_.process_instance_id,
            definition_id=task_.process_definition_id,
            # definition_key=task_.process_definition_key,
            task_assignee=task_.assignee,
            create_time=util.parse_time(task_.created),
            node_id=task_.task_definition_key,
            node_name=task_.name,
            task_status=ApprovalTaskStatus.PENDING.value,
        )

        return process_task

    @classmethod
    def packTaskList(cls, task_list, process_definition_key):
        process_tasks = []
        for task_ in task_list:
            process_task = ProcessTask.packTask(task_)
            if process_task is not None:
                process_task.definition_key = process_definition_key
                process_tasks.append(process_task)
        return process_tasks

    @classmethod
    def packHistoryTaskList(cls, task_list):
        process_tasks = []
        for task_ in task_list:

            process_task = ProcessTask(
                id=task_.id_,
                task_id=task_.id_,
                task_name=task_.name,
                instance_id=task_.process_instance_id,
                definition_id=task_.process_definition_id,
                definition_key=task_.process_definition_key,
                task_assignee=task_.assignee,
                create_time=util.parse_time(task_.start_time),
                end_time=util.parse_time(task_.end_time),
                task_status=pack_task_status(task_.id_),
                node_id=task_.task_definition_key,
                node_name=task_.name,
                delete_reason=task_.delete_reason,
            )
            process_tasks.append(process_task)
        return process_tasks
