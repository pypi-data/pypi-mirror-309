import json

import pycamunda
import pycamunda.task
from mybpm.api.model.query_params import *
from mybpm.api.model.query_params import GetInstanceListRequest
from mybpm.camunda import histaskinst
from mybpm.constant import *
from mybpm.model.definition import FormItem, NodeDefinition
from mybpm.model.task import ProcessTask
from mybpm.service import process_instance, process_task, process_variables
from mybpm.service.process_definition import BpmSystem
from mybpm.utils import util

test_definition_code = "Process1851522678232739840"


class MyApproval:
    @classmethod
    def get_approval_definition_form(cls, definition_code: str):
        """
        获取审批定义表单
        """
        definition_code = test_definition_code
        process_definition = BpmSystem.get_process_definition(definition_code)
        if process_definition is None:
            raise Exception("审批定义不存在")
        form_items = process_definition.formItems
        form_perms = process_definition.process.props.formPerms
        hidden_ids = {perm.id for perm in form_perms if perm.perm == FormPermType.HIDDEN.value}
        resp = GetApprovalDefinitionFormResp(form=[item for item in form_items if item.id not in hidden_ids])
        return resp

    @classmethod
    def get_instance_biz_info(cls, usr_email, instance_id: str):
        """
        获取审批实例业务信息
        """
        instance = process_instance.get_instance_by_instance_id(instance_id)
        variables = process_variables.get_variables_by_instance_id(instance_id)
        if not variables or not instance:
            return {}
        form_data = json.loads(variables[FORM_VAR])
        print(form_data)
        form_value = [FormItem(**item) for item in form_data]

        process_definition = BpmSystem.get_process_definition(instance.definition_key)
        form_item = process_definition.formItems
        current_task = process_task.get_latest_task_by_instance_id(instance_id)
        if current_task is None:
            return {}
        current_node = NodeDefinition.get_process_node_by_node_id(process_definition.process, current_task.node_id)
        form_perms = current_node.props.formPerms
        edit_ids = {perm.id for perm in form_perms if perm.perm == FormPermType.EDITABLE.value}
        hidden_ids = {perm.id for perm in form_perms if perm.perm == FormPermType.HIDDEN.value}
        result = GetInstanceBizInfoResp()
        result.instance = instance
        result.form_info = [item for item in form_value if item.id not in hidden_ids]
        result.todo_form_info = [item for item in form_item if item.id in edit_ids]
        return result

    @classmethod
    def verify_approval_user(cls, cur_user_email, definition_code):
        process_definition = BpmSystem.get_process_definition(definition_code)
        if process_definition is None:
            raise Exception("审批定义不存在")
        process = process_definition.process
        root_node = NodeDefinition.get_process_node_by_node_id(process, "root")
        vievers = root_node.props.assignedUser
        for viever in vievers:
            if viever.type == UserType.department.value:
                pass
                # department_id = item.id
                # user_list = lark_contact_module.get_users_by_department_id(
                #     department_id, ContactDepartmentIDType.department_id.value
                # )
                # if cur_user_id in [item.user_id for item in user_list]:
                #     return
            elif viever.type == UserType.user.value:
                if cur_user_email == viever.name:
                    return
        raise Exception(f"当前用户<{cur_user_email}>无权创建审批流程")

    @classmethod
    def create_approval(cls, definition_code, formData, user_email):
        """
        创建审批实例
        """
        definition_code = test_definition_code
        cls.verify_approval_user(user_email, definition_code)
        processDefinition = BpmSystem.get_process_definition(definition_code)
        form_items_define = processDefinition.formItems

        item_mapping = {item.id: item for item in form_items_define}

        for form_entry in formData:
            form_id = form_entry.get("id")
            if form_id in item_mapping:
                form_entry["custom_id"] = item_mapping[form_id].custom_id
                form_entry["name"] = item_mapping[form_id].name

        resp = process_instance.start_process(definition_code, formData, user_email)
        return resp

    @classmethod
    def list_approval_instance(cls, req: GetInstanceListRequest):
        """
        获取审批实例列表
        """
        instances, instance_task_map = process_instance.get_process_instance_list(req)
        _list = []
        resp = {}

        for instance in instances:
            if instance.creator is None:
                continue
            has_todo = process_task.check_user_has_todo_task(
                instance.instance_id, instance_task_map[instance.instance_id]
            )
            username = instance.creator.split("@")[0]
            src_dict = {"src_type": "USER", "src_info": {"USER": {"username": username, "email": instance.creator}}}
            _list.append(
                {
                    **{"created_by": src_dict},
                    **(instance.dict()),
                    **{"has_todo": has_todo},
                    **{
                        "task": instance_task_map[instance.instance_id][0].dict()
                        if instance_task_map.get(instance.instance_id)
                        else {}
                    },
                }
            )

        resp["results"] = _list
        return resp

    @classmethod
    def approval_instance_detail(cls, instance_id):
        """
        获取审批实例详情
        """
        instance = process_instance.get_instance_by_instance_id(instance_id)
        if not instance:
            return None

        getlist = histaskinst.GetTasks(url=URL_CAMUNDA_ENGINE, process_instance_id=instance_id)
        task_list = ProcessTask.packHistoryTaskList(getlist())
        completed_task = [task for task in task_list if task.task_status != ApprovalTaskStatus.PENDING.value]
        completed_task_timeline = sorted(completed_task, key=lambda task: task.end_time)
        res = ApprovalInstanceDetailResp(
            instance_code=instance_id,
            approval_name=instance.definition_name,
            start_time=instance.create_time,
            end_time=instance.end_time,
            status=instance.current_status,
        )
        res.task_list = ApprovalInstanceDetailResp.pack_task_list(task_list)

        for task_ in completed_task_timeline:
            if task_.task_status == ApprovalTaskStatus.DONE.value:
                continue
            if task_.node_id == "root":
                user_email = util.get_instance_start_user_email(instance_id)
                res.timeline.append(
                    TimeLineItem(
                        # task_id=task_.task_id,
                        user_email=task_.task_assignee,
                        user_name=util.trans_email_to_username(task_.task_assignee),
                        create_time=task_.create_time,
                        node_key=task_.node_id,
                        type="START",
                    )
                )
            else:
                type = None
                if task_.task_status == ApprovalTaskStatus.APPROVED.value:
                    type = ApprovalTimeLineEventType.PASS.value
                if task_.task_status == ApprovalTaskStatus.REJECTED.value:
                    type = ApprovalTimeLineEventType.REJECT.value

                timeline_now = TimeLineItem(
                    task_id=task_.task_id,
                    user_email=task_.task_assignee,
                    user_name=util.trans_email_to_username(task_.task_assignee),
                    create_time=task_.create_time,
                    node_key=task_.node_id,
                    type=type,
                    comment=process_task.get_comment_by_task_id(task_.task_id),
                )
                if task_.task_status == ApprovalTaskStatus.CANCELED.value:
                    user_email = process_variables.get_instance_variables_by_key(instance_id, APPLY_USER_ID)
                    timeline_now.type = ApprovalTimeLineEventType.CANCEL.value
                    timeline_now.user_email = user_email
                    timeline_now.user_name = util.trans_email_to_username(user_email)
                    res.timeline.append(timeline_now)
                    break

                res.timeline.append(timeline_now)

        return res

    @classmethod
    def approval_instance_preview(cls, instance_id):
        """
        获取审批实例流程预览
        """
        instance = process_instance.get_instance_by_instance_id(instance_id)
        if not instance:
            return None
        definition_code = instance.definition_key
        resp = ApprovalInstancePreviewResp()
        getlist = histaskinst.GetTasks(url=URL_CAMUNDA_ENGINE, process_instance_id=instance_id, unfinished=True)
        pending_tasks = ProcessTask.packHistoryTaskList(getlist())
        if len(pending_tasks) == 0:
            return resp
        pending_task = pending_tasks[0]

        processDefinition = BpmSystem.get_process_definition(definition_code)
        if not processDefinition:
            return resp
        process = processDefinition.process
        preview_node_now = NodeDefinition.get_process_node_by_node_id(process, pending_task.node_id)
        preview_nodes = NodeDefinition.get_process_node_list(preview_node_now)
        for node in preview_nodes:
            preview_node = PreviewNode.assemble_preview_node(node, pending_task.task_id, pending_task.instance_id)
            resp.preview_nodes.append(preview_node)
        return resp

    @classmethod
    def agree_approval_task(cls, req: AgreeTaskRequest):
        email = req.user_email
        comment = req.general_reason or req.comment
        current_task = process_task.get_task_by_task_id(req.task_id)
        if not current_task:
            current_task = process_task.get_current_task(req.instance_id, email)
        if not current_task:
            raise Exception("未找到当前任务")
        if comment:
            pycamunda.task.CommentCreate(url=URL_CAMUNDA_ENGINE, task_id=current_task.task_id, message=comment)()
        process_variables = {}
        if req.form is not None and len(req.form) != 0:
            process_variables[FORM_VAR] = util.parse_upadte_form(req.instance_id, req.form)
            processed_form = {item["id"]: item["value"] for item in req.form}
            process_variables.update(processed_form)
        process_task.complete_task(current_task, process_variables)

    @classmethod
    def reject_approval_task(cls, req: RejectTaskRequest):
        email = req.user_email
        comment = req.general_reason or req.comment
        current_task = process_task.get_task_by_task_id(req.task_id)
        if not current_task:
            current_task = process_task.get_current_task(req.instance_id, email)
        if not current_task:
            return None
        if comment:
            pycamunda.task.CommentCreate(url=URL_CAMUNDA_ENGINE, task_id=current_task.task_id, message=comment)()
        pycamunda.processinst.VariablesUpdate(
            url=URL_CAMUNDA_ENGINE,
            process_instance_id=req.instance_id,
            var_name=PROCESS_STATUS,
            value=BpmInstanceStatus.REJECTED.value,
            type_="String",
        )()
        process_task.set_task_status(current_task, ApprovalTaskStatus.REJECTED.value)
        pycamunda.processinst.Delete(url=URL_CAMUNDA_ENGINE, id_=req.instance_id)()

    @classmethod
    def cancel_instance(cls, req: CancelInstanceRequest):
        email = req.user_email
        variables = process_variables.get_variables_by_instance_id(req.instance_id)
        creator = variables.get(APPLY_USER_ID)
        if creator != email:
            raise Exception("无权限取消")

        pycamunda.processinst.VariablesUpdate(
            url=URL_CAMUNDA_ENGINE,
            process_instance_id=req.instance_id,
            var_name=PROCESS_STATUS,
            value=BpmInstanceStatus.CANCELED.value,
            type_="String",
        )()
        tasks = process_task.get_task_list_by_instance_id(req.instance_id, req.definition_code)
        for t in tasks:
            process_variables.set_task_variable(t.task_id, TASK_STATUS, ApprovalTaskStatus.CANCELED.value)
        pycamunda.processinst.Delete(url=URL_CAMUNDA_ENGINE, id_=req.instance_id)()

    @classmethod
    def get_approval_summary(cls, process_definition_key, user_email, status):
        """
        获取审批数量统计
        """
        process_definition_key = test_definition_code
        req = GetInstanceListRequest(definition_key=process_definition_key, user_email=user_email, status=status)
        res = cls.list_approval_instance(req).get("results", [])
        return len(res)

    # @classmethod
    # def rollback_task(cls,req:ApprovalRollbackRequest):
    #     user_email = req.user_email
    #     comment = req.general_reason or req.comment
    #     current_task = process_task.get_task_by_task_id(req.task_id)
    #     if not current_task:
    #         current_task = process_task.get_current_task(req.instance_id, user_email)
    #     if not current_task:
    #         raise Exception(f"当前用户<email: {user_email}>没有待审批的任务，无法回退")
    #     if comment:
    #         task.CommentCreate(url=URL_CAMUNDA_ENGINE, task_id=current_task.task_id, message=comment)()
    #     process_task.set_task_status(current_task, ApprovalTaskStatus.ROLLBACK.value)
    #     processinst.Delete(url=URL_CAMUNDA_ENGINE, id_=req.instance_id)()
