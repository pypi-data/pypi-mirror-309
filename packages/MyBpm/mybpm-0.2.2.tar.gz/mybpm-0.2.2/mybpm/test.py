import json
import traceback

from pycamunda import auth, deployment, processdef, processinst, task, user
# from mybpm.service.process_instance import get_form_value_by_instance_id
from mybpm.api.approval_center import MyApproval
from mybpm.constant import *
from mybpm.service import process_task
from mybpm.service.process_definition import BpmSystem
from utils.query_params import ApprovalAgreeRequest, ApprovalPreviewRequest, ApprovalRejectRequest

from app.mybpm.api.model.query_params import GetInstanceListRequest

formData = [
    {"id": "widget17150720090240001", "type": "input", "value": "test"},
    {"id": "widget17150720206220001", "type": "input", "value": "jxy"},
    {"id": "widget17180879911840001", "type": "textarea", "value": "瘾夀股票进取02号私募证券投资基金"},
]


# req = GetInstanceListRequest(definition_key="Process1851522678232739840",user_email="100001",status="todo")
# print(MyApproval.list_approval_instance(req))
# print(processinst.GetList(url=URL_CAMUNDA_ENGINE, process_instance_ids="1851523116063551488")()[0])
definition_id = "Process1851522678232739840"
email = "xinyu.jiang@metabit-trading.com"
ordering = "-start_time"
# MyApproval.create_approval("Process1851522678232739840", formData,email)
# req = GetInstanceListRequest(definition_key=definition_id, user_email=email, status="todo")
# if ordering:
#     if ordering[0] == "-":
#         req.ascending = False
#         req.sort_by = ordering[1:]
#     else:
#         req.ascending = True
#         req.sort_by = ordering

# preview_req = ApprovalPreviewRequest(task_id="1855867864458997760", user_id="xinyu.jiang@metabit-trading.com")
# print(MyApproval.approval_instance_detail("1856624482788380672"))
# print(MyApproval.approval_instance_preview("1855867864458997760"))
# taskList = process_task.get_task_list_by_instance_id("1853675623904800768")
# print(f"当前任务为:{taskList[0].task_name}")
# req= ApprovalAgreeRequest(approval_code="8B9959CE-BB62-48B1-8ABA-19948D8E8E8B",task_id="1856988266358956032",user_email = "xinyu.jiang@metabit-trading.com")
# print(MyApproval.agree_approval_task(req))
# taskList = process_task.get_task_list_by_instance_id("1853675623904800768")
# req=ApprovalRejectRequest(instance_id ="1855894073830027264")
# print(processinst.Delete(url=URL_CAMUNDA_ENGINE, id_="1853675623904800768")())
# print(BpmSystem.delete_process_instance("1855894073830027264"))
# print(process_task.get_latest_task_by_instance_id("1856526740481155072"))
# req = GetInstanceListRequest(
#     definition_key="Process1851522678232739840", user_email="xinyu.jiang@metabit-trading.com", status="todo"
# )
# print(MyApproval.list_approval_instance(req))

# modify_instance = processinst.Modify(url=URL_CAMUNDA_ENGINE, id_='1857256710564274176')
# modify_instance.add_before_activity_instruction(id_='node_722630724838#multiInstanceBody')
# print(modify_instance())
# cancel_instance = processinst.Modify(url=URL_CAMUNDA_ENGINE, id_='1857256710564274176')
# cancel_instance.add_cancel_activity_instruction(id_ = 'node_723339237633#multiInstanceBody')
# print(cancel_instance())


# modify_vars = task.LocalVariablesModify(url=URL_CAMUNDA_ENGINE, task_id='1856956341518917635')
# modify_vars.add_variable(name='anotherVar', value='aVal', type_='String')
# print(modify_vars())
# complete_task_func = task.Complete(url=URL_CAMUNDA_ENGINE, id_="1857257287075553283")
# complete_task_func()
# get_var = task.LocalVariablesGet(
#         url=URL_CAMUNDA_ENGINE, task_id='1856956341518917635', var_name='anotherVar'
# )
# print(get_var())
# print(MyApproval.get_instance_biz_info("","1857294580960256000"))
print(BpmSystem.get_process_definition("Process1851522678232739840"))
