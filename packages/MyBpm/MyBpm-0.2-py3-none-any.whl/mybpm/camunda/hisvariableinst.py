# -*- coding: utf-8 -*-

"""This module provides access to the external task REST api of Camunda."""

from __future__ import annotations

import dataclasses
import typing

import pycamunda
import pycamunda.base
import pycamunda.batch
import pycamunda.variable
from pycamunda.request import QueryParameter

URL_SUFFIX = "/history/variable-instance"


__all__ = ["GetVariables"]


@dataclasses.dataclass
class HistoryVariableInstance:
    """Data class of HistoryTaskInstance returned by the REST api of Camunda."""

    id_: str
    name: str
    process_definition_id: str
    process_definition_key: str
    process_instance_id: str
    activity_instance_id: str
    create_time: str
    task_id: str
    value: any
    type: str
    valueInfo: object

    @classmethod
    def load(cls, data: typing.Mapping[str, typing.Any]) -> HistoryVariableInstance:
        history_variable_instance = cls(
            id_=data["id"],
            name=data["name"],
            process_definition_id=data["processDefinitionId"],
            process_definition_key=data["processDefinitionKey"],
            process_instance_id=data["processInstanceId"],
            activity_instance_id=data["activityInstanceId"],
            create_time=data["createTime"],
            task_id=data["taskId"],
            value=data["value"],
            type=data["type"],
            valueInfo=data["valueInfo"],
        )
        return history_variable_instance


class GetVariables(pycamunda.base.CamundaRequest):
    variable_name = QueryParameter("variableName")
    variable_value = QueryParameter("variableValue")
    include_deleted = QueryParameter("includeDeleted")

    task_id_in = QueryParameter("taskIdIn")
    process_instance_id = QueryParameter("processInstanceId")
    process_definition_id = QueryParameter("processDefinitionId")
    process_definition_key = QueryParameter("processDefinitionKey")

    def __init__(
        self,
        url: str,
        variable_name: str = None,
        variable_value: object = None,
        include_deleted: bool = None,
        task_id_in: str = None,
        process_instance_id: str = None,
        process_definition_id: str = None,
        process_definition_key: str = None,
    ):
        """Query for a list of external tasks using a list of parameters. The size of the result set
        can be retrieved by using the Get Count request.
        :param url: Camunda Rest engine URL.
        :param id_: Filter by the id of the external task.
        :param process_instance_id: Filter by the process_instance_id
        """
        super().__init__(url=url + URL_SUFFIX)
        self.variable_name = variable_name
        self.variable_value = variable_value
        self.include_deleted = include_deleted
        self.task_id_in = task_id_in
        self.process_instance_id = process_instance_id
        self.process_definition_id = process_definition_id
        self.process_definition_key = process_definition_key

    def __call__(self, *args, **kwargs) -> typing.Tuple[HistoryVariableInstance]:
        """Send the request."""
        response = super().__call__(pycamunda.base.RequestMethod.GET, *args, **kwargs)
        return tuple(HistoryVariableInstance.load(data_json) for data_json in response.json())
