import datetime
import json
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, root_validator, validator
from mybpm.camunda import hisvariableinst
from mybpm.constant import START_USER_INFO, URL_CAMUNDA_ENGINE, AssigneeType
from mybpm.model.definition import FormItem, NodeDefinition
from mybpm.model.instance import ProcessInstance
from mybpm.service.process_definition import BpmSystem
from mybpm.utils import util


# from utils.query_params import GenericQuery


class GetInstanceListRequest(BaseModel):
    definition_key: str = None
    status: str = None
    user_email: str = None
    sort_by: str = None
    ascending: str = None
    filtering: Dict[str, Any] = None
    searching: Dict[str, Any] = None


class TimeLineItem(BaseModel):
    task_id: str = None
    type: str = None
    create_time: str = None
    node_key: str = None
    user_id: str = None
    user_name: str = None
    user_email: str = None
    comment: str = None


class ApprovalDetailTask(BaseModel):
    id: str
    user_id: str = None
    status: str
    node_name: str
    type: str = None
    start_time: str
    end_time: str
    user_name: str = None
    user_email: str = None
    node_type: str = None
    node_key: str = None


class AgreeTaskRequest(BaseModel):
    user_email: str = None
    instance_id: str = None
    form: List[Any] = None
    comment: str = None
    general_reason: str = None
    task_id: str = None


class RejectTaskRequest(BaseModel):
    user_email: str = None
    instance_id: str = None
    comment: str = None
    general_reason: str = None
    task_id: str = None


class CancelInstanceRequest(BaseModel):
    definition_code: str = None
    instance_id: str = None
    user_email: str = None
    general_reason: str = None


class ApprovalInstanceDetailResp(BaseModel):
    instance_code: str
    approval_name: str
    start_time: str
    end_time: str = None
    status: str
    task_list: List[ApprovalDetailTask] = []
    timeline: List[TimeLineItem] = []

    @classmethod
    def pack_task_list(cls, task_list):

        res = []
        if task_list is None or len(task_list) == 0:
            return []

        definition_code = task_list[0].definition_key
        processDefinition = BpmSystem.get_process_definition(definition_code)
        if not processDefinition:
            return []
        process = processDefinition.process

        for task in task_list:
            detail_task = ApprovalDetailTask(
                id=task.id,
                status=task.task_status,
                node_name=task.node_name,
                start_time=task.create_time,
                end_time=task.end_time,
                user_name=util.trans_email_to_username(task.task_assignee),
                user_email=task.task_assignee,
                node_key=task.node_id,
                node_type="approve",
            )
            # user = lark_contact_module.get_users_batch_by_email("user_id", email_list=[task.task_assignee])
            # detail_task.user_id = user[0].user_id
            task_node = NodeDefinition.get_process_node_by_node_id(process, task.node_id)
            detail_task.type = task_node.props.mode
            res.append(detail_task)
        return res


class UserResp(BaseModel):
    user_name: str = None
    user_email: str = None
    user_id: str = None
    open_id: str = None


class PreviewNode(BaseModel):
    node_id: str
    node_name: str
    node_type: str = None
    custom_node_id: str = None
    user_list: List[UserResp] = []
    is_empty_logic: bool = False
    is_approver_type_free: bool = False

    @classmethod
    def assemble_preview_node(cls, node_def: NodeDefinition, task_id: str, instance_id: str):
        preview_node = PreviewNode(
            node_id=node_def.id,
            node_name=node_def.name,
            node_type=node_def.props.mode,
        )
        preview_node.user_list = []
        assignedType = node_def.props.assignedType
        if assignedType is None:
            return preview_node

        elif assignedType == AssigneeType.ASSIGN_USER.value:
            for user in node_def.props.assignedUser:
                user_resp = UserResp(
                    user_name=util.trans_email_to_username(user.name),
                    user_email=user.name,
                )
                preview_node.user_list.append(user_resp)
        elif assignedType == AssigneeType.SELF.value:
            user_email = util.get_instance_start_user_email(instance_id)
            preview_node.user_list.append(
                UserResp(
                    user_name=util.trans_email_to_username(user_email),
                    user_email=user_email,
                )
            )
        elif assignedType == AssigneeType.FORM_USER.value:
            getlist = hisvariableinst.GetVariables(
                url=URL_CAMUNDA_ENGINE, variable_name=node_def.props.formUser, process_instance_id=instance_id
            )
            variables = getlist()
            if len(variables) == 0:
                return preview_node
            user_list_str = variables[0].value
            user_dicts = json.loads(user_list_str)
            for user in user_dicts:
                user_resp = UserResp(
                    user_name=util.trans_email_to_username(user.get("name")),
                    user_email=user.get("name"),
                )
                preview_node.user_list.append(user_resp)
        return preview_node


class ApprovalInstancePreviewResp(BaseModel):
    preview_nodes: List[PreviewNode] = []


class GetApprovalDefinitionFormResp(BaseModel):
    form: List[FormItem] = []


class GetInstanceBizInfoResp(BaseModel):
    instance: ProcessInstance = None
    form_info: List[FormItem] = []
    todo_form_info: List[FormItem] = []
