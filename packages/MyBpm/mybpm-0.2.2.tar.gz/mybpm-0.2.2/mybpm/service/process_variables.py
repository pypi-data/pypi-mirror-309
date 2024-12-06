import pycamunda
from mybpm.camunda import hisvariableinst
from mybpm.constant import *


def get_variables_by_instance_id(instance_id):
    getlist = hisvariableinst.GetVariables(url=URL_CAMUNDA_ENGINE, process_instance_id=instance_id)
    variables = getlist()
    variable_map = {var.name: var.value for var in variables}
    return variable_map


def get_instance_variables_by_key(instance_id, key):
    getlist = hisvariableinst.GetVariables(url=URL_CAMUNDA_ENGINE, variable_name=key, process_instance_id=instance_id)
    variables = getlist()
    if len(variables) == 0:
        return None
    return variables[0].value


def set_task_variable(task_id, variable_name, variable_value):
    modify_vars = pycamunda.task.LocalVariablesModify(url=URL_CAMUNDA_ENGINE, task_id=task_id)
    modify_vars.add_variable(name=variable_name, value=variable_value, type_="String")
    modify_vars()
