import json
import re
from datetime import datetime
from mybpm.constant import FORM_VAR
from mybpm.service import process_variables


def trans_email_to_username(email):
    if email is None:
        return ""
    return email.split("@")[0]


def parse_time(date_str):
    if date_str is None:
        return 0

    # 检查是否为 datetime 对象
    if isinstance(date_str, datetime):
        # 将 datetime 对象转换为毫秒
        return int(date_str.timestamp() * 1000)

    # 检查是否为字符串对象
    if isinstance(date_str, str):
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        return int(dt.timestamp() * 1000)


def parse_update_form(instance_id, form_update):
    variables = process_variables.get_variables_by_instance_id(instance_id)
    if not variables or not variables.get(FORM_VAR):
        return ""
    form_origin = json.loads(variables[FORM_VAR])

    update_form_dict = {item["id"]: item for item in form_origin}

    for item in form_update:
        if item["id"] in update_form_dict:
            form_update[item["id"]].update(item)
        else:
            form_origin.append(item)

    return json.dumps(form_origin)

