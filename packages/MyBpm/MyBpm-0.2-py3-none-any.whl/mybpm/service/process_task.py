import traceback

import pycamunda
# from pycamunda import task
from mybpm.camunda import histaskinst
from mybpm.constant import *
from mybpm.constant import ApprovalTaskStatus
from mybpm.model.definition import NodeDefinition
from mybpm.model.task import ProcessTask
from mybpm.service import process_variables
from mybpm.service.process_definition import BpmSystem


def set_task_status_for_agree(task):
    node_id = task.node_id
    processDefinition = BpmSystem.get_process_definition(task.definition_key)
    current_node = NodeDefinition.get_process_node_by_node_id(processDefinition.process, node_id)
    node_type = current_node.props.mode
    process_variables.set_task_variable(task.task_id, TASK_STATUS, ApprovalTaskStatus.APPROVED.value)
    if node_type == "OR":  # 或签
        tasks = get_task_list_by_instance_id(task.instance_id, task.definition_key)
        for t in tasks:
            if t.task_id == task.task_id or t.node_id != node_id:
                continue
            process_variables.set_task_variable(t.task_id, TASK_STATUS, ApprovalTaskStatus.DONE.value)


def set_task_status(task, status):
    process_variables.set_task_variable(task.task_id, TASK_STATUS, status)
    tasks = get_task_list_by_instance_id(task.instance_id, task.definition_key)
    for t in tasks:
        if t.task_id == task.task_id:
            continue
        process_variables.set_task_variable(t.task_id, TASK_STATUS, ApprovalTaskStatus.DONE.value)


def complete_task(task, variables=None):
    if not task:
        return None
    task_id = task.task_id
    set_task_status_for_agree(task)
    complete_task_func = pycamunda.task.Complete(url=URL_CAMUNDA_ENGINE, id_=task_id)
    if variables is not None:
        for key, value in variables.items():
            complete_task_func.add_variable(name=key, value=value, type_="String")
    complete_task_func()


def get_task_list_by_instance_id(process_instance_id, process_definition_key):
    getlist = pycamunda.task.GetList(url=URL_CAMUNDA_ENGINE, process_instance_id=process_instance_id, active=True)
    tasktur = getlist()
    return ProcessTask.packTaskList(tasktur, process_definition_key)


def get_latest_task_by_instance_id(process_instance_id):
    getlist = histaskinst.GetTasks(url=URL_CAMUNDA_ENGINE, process_instance_id=process_instance_id)
    task_list = ProcessTask.packHistoryTaskList(getlist())
    if len(task_list) == 0:
        return None
    task_list_sorted = sorted(task_list, key=lambda task: (task.end_time != 0, -task.end_time))
    return task_list_sorted[0]


# 获取待办/已办任务
def get_assigneed_task_list(process_definition_key, user_email, condition="all"):
    finished = unfinished = None
    if condition == "todo":
        unfinished = True
    elif condition == "done":
        finished = True
    print(
        f"process_definition_key:{process_definition_key},user_email:{user_email},finished:{finished},unfinished:{unfinished}"
    )
    getlist = histaskinst.GetTasks(
        url=URL_CAMUNDA_ENGINE,
        process_definition_key=process_definition_key,
        task_assignee=user_email,
        finished=finished,
        unfinished=unfinished,
    )
    task_list = getlist()
    return ProcessTask.packHistoryTaskList(task_list)


def get_current_task(process_instance_id, user_email):
    getlist = histaskinst.GetTasks(
        url=URL_CAMUNDA_ENGINE, process_instance_id=process_instance_id, task_assignee=user_email, unfinished=True
    )
    task_list = ProcessTask.packHistoryTaskList(getlist())
    if len(task_list) == 0:
        return None
    return task_list[0]


def get_task_by_task_id(task_id):
    if not task_id:
        return None
    getlist = histaskinst.GetTasks(url=URL_CAMUNDA_ENGINE, task_id=task_id)
    task_list = ProcessTask.packHistoryTaskList(getlist())
    if len(task_list) == 0:
        return None
    return task_list[0]


def get_comment_by_task_id(task_id):
    comments = pycamunda.task.CommentGetList(url=URL_CAMUNDA_ENGINE, task_id=task_id)()
    if len(comments) == 0:
        return ""
    return comments[0].message


def check_user_has_todo_task(cls, task_list):
    for task in task_list:
        if task.task_status == ApprovalTaskStatus.PENDING.value:
            process_definition = BpmSystem.get_process_definition(task.definition_key)
            current_node = NodeDefinition.get_process_node_by_node_id(process_definition.process, task.node_id)
            form_item = current_node.props.formPerms
            for item in form_item:
                if item.perm == FormPermType.EDITABLE.value:
                    return True
    return False
