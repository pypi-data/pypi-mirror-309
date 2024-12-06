import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, ForwardRef, List, Optional, Union

from pydantic import BaseModel, Field, root_validator
from mybpm.camunda import hisprocessinst
from mybpm.constant import PROCESS_STATUS, ApprovalInstanceStatus, BpmInstanceStatus
from mybpm.model.definition import FormItem
from mybpm.service import process_variables
from mybpm.utils import util


def pack_instance_status(instance):
    if instance.state == BpmInstanceStatus.COMPLETED.value:
        return ApprovalInstanceStatus.APPROVED.value
    if instance.state == BpmInstanceStatus.ACTIVE.value:
        return ApprovalInstanceStatus.PENDING.value
    if instance.state == BpmInstanceStatus.EXTERNALLY_TERMINATED.value:
        variables = process_variables.get_variables_by_instance_id(instance.id_)
        if variables.get(PROCESS_STATUS) == BpmInstanceStatus.REJECTED.value:
            return ApprovalInstanceStatus.REJECTED.value
        if variables.get(PROCESS_STATUS) == BpmInstanceStatus.CANCELED.value:
            return ApprovalInstanceStatus.CANCELED.value
    return ApprovalInstanceStatus.PENDING.value


class ProcessInstance(BaseModel):
    definition_id: str
    definition_key: str
    definition_name: str = None
    instance_id: str
    current_node_id: str = None
    current_status: str
    create_time: int
    update_time: int = None
    end_time: int = None
    creator: Optional[str] = None
    key_info: str = None
    todo_user_list: List[str] = None
    done_user_list: List[str] = None

    @classmethod
    def packHistoryProcessInstance(cls, instance_list):
        process_instances = []
        for instance_ in instance_list:

            process_task = ProcessInstance(
                definition_id=instance_.process_definition_id,
                definition_key=instance_.process_definition_key,
                definition_name=instance_.process_definition_name,
                instance_id=instance_.id_,
                current_node_id=instance_.start_activity_id,
                current_status=pack_instance_status(instance_),
                create_time=util.parse_time(instance_.start_time),
                end_time=util.parse_time(instance_.end_time),
                creator=instance_.start_user_id,
            )
            process_instances.append(process_task)
        return process_instances

    @classmethod
    def sort_process_instances(cls, instances, sort_by: str, ascending: bool = True):
        if not sort_by:
            return instances
        return sorted(instances, key=lambda instance: getattr(instance, sort_by), reverse=not ascending)
