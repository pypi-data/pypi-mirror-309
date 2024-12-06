import json
import traceback
from collections import defaultdict

from pycamunda import processdef
from mybpm.camunda import hisprocessinst, histaskinst, hisvariableinst
from mybpm.constant import *
from mybpm.constant import ApprovalInstanceStatus, ApprovalTaskStatus, ApprovalTimeLineEventType
from mybpm.model.instance import ProcessInstance
from mybpm.model.task import ProcessTask
from mybpm.service import process_task, process_variables
from mybpm.utils import util

from mybpm.api.model.query_params import GetInstanceListRequest
from mybpm.model.definition import NodeDefinition
from mybpm.service.process_definition import BpmSystem

# from utils.log import app_logger as logger


def start_process(process_definition_key, form, user_email):
    try:
        process_variables = {}
        # 直接将值放入字典
        process_variables[FORM_VAR] = json.dumps(form)
        process_variables[PROCESS_STATUS] = BpmInstanceStatus.PENDING.value
        process_variables[START_USER_INFO] = json.dumps(
            {"id": user_email, "name": util.trans_email_to_username(user_email)}
        )
        process_variables[APPLY_USER_ID] = user_email
        processed_form = {item["id"]: str(item["value"]) for item in form}
        process_variables.update(processed_form)
        start_instance = processdef.StartInstance(
            url=URL_CAMUNDA_ENGINE, key=process_definition_key, with_variables_in_return=True
        )
        start_instance.start_user_id = user_email
        for key, value in process_variables.items():
            start_instance.add_variable(name=key, value=value, type_="String")

        # 执行请求，启动流程实例
        response = start_instance()
        process_instance_id = response.id_
        print(f"流程实例已创建，实例ID为: {response.id_}")
        # 手动完成root任务，即发起任务
        taskList = process_task.get_task_list_by_instance_id(process_instance_id, process_definition_key)
        process_task.complete_task(taskList[0])
        return process_instance_id
    except Exception as e:
        print(f"创建流程时出错: {e}")
        traceback.print_exc()
        raise e


def get_instance_by_instance_id(instance_id):
    getlist = hisprocessinst.GetList(url=URL_CAMUNDA_ENGINE, process_instance_id=instance_id)
    instance_list = getlist()
    if len(instance_list) == 0:
        return None
    return ProcessInstance.packHistoryProcessInstance(instance_list)[0]


def get_submit_instance_list(process_definition_key, user_email):
    getlist = hisprocessinst.GetList(
        url=URL_CAMUNDA_ENGINE, process_definition_key=process_definition_key, started_by=user_email
    )
    process_inst_list = getlist()
    return ProcessInstance.packHistoryProcessInstance(process_inst_list)


def get_instance_update_time(instance_id, instance_task_map):

    # 获取所有任务的 start_time 和 end_time，考虑 end_time 可能为 None
    times = [task.create_time for task in instance_task_map[instance_id] if task.create_time is not None]
    times += [task.update_time for task in instance_task_map[instance_id] if task.update_time is not None]
    times += [task.end_time for task in instance_task_map[instance_id] if task.end_time is not None]
    # 返回最大时间作为最新更新时间
    update_time = max(times) if times else None
    return update_time if update_time else 0


def get_process_instance_list(req: GetInstanceListRequest):
    """
    获取审批实例列表
    """
    instances = []
    if req.status == "submit":
        instances = get_submit_instance_list(req.definition_key, req.user_email)
        instance_ids = {instance.instance_id for instance in instances}  # 使用集合来去重
        getlist = histaskinst.GetTasks(url=URL_CAMUNDA_ENGINE, process_instance_ids=instance_ids)
        process_tasks = ProcessTask.packHistoryTaskList(getlist())
    else:
        process_tasks = process_task.get_assigneed_task_list(req.definition_key, req.user_email, req.status)
        instance_ids = {task.instance_id for task in process_tasks}  # 使用集合来去重
        instance_ids_string = ",".join(instance_ids)  # 转换成逗号分隔的字符串
        getlist = hisprocessinst.GetList(url=URL_CAMUNDA_ENGINE, process_instance_ids=instance_ids_string)
        instances = ProcessInstance.packHistoryProcessInstance(getlist())
    # logger.info(f"[list_approval_instance] process_tasks:{process_tasks},instances:{instances}")

    instance_task_map = defaultdict(list)
    for task in process_tasks:
        instance_task_map[task.instance_id].append(task)
    for instance in instances:
        variables = process_variables.get_variables_by_instance_id(instance.instance_id)
        # print(variables.get(FORM_VAR))
        instance.key_info = json.loads(variables.get(FORM_VAR))
        instance.creator = variables.get(APPLY_USER_ID)
        instance.update_time = get_instance_update_time(instance.instance_id, instance_task_map)

    return ProcessInstance.sort_process_instances(instances, req.sort_by, req.ascending), instance_task_map




def parse_timeline_type(instance_id, task_status):
    if task_status == ApprovalTaskStatus.APPROVED.value:
        return ApprovalTimeLineEventType.PASS.value
    if task_status == ApprovalTaskStatus.REJECTED.value:
        return ApprovalTimeLineEventType.REJECT.value
    if task_status == ApprovalTaskStatus.CANCELED.value:
        return ApprovalTimeLineEventType.CANCEL.value
    return None
