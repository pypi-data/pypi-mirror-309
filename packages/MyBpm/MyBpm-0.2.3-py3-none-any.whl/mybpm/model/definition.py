import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, ForwardRef, List, Optional, Union

from pydantic import BaseModel, Field, root_validator


class AssignedUser(BaseModel):
    id: int
    name: str  # 实际存的用户邮箱
    type: str
    sex: Optional[bool] = None
    selected: bool = False


class FormPerm(BaseModel):
    id: str
    title: str
    required: bool
    perm: str


# 时间限制和处理信息的数据结构


class Timeout(BaseModel):
    unit: str
    value: int


@dataclass
class Notify:
    once: bool
    hour: int


@dataclass
class Handler:
    type: str
    notify: Notify


@dataclass
class TimeLimit:
    timeout: Timeout
    handler: Handler


@dataclass
class Nobody:
    handler: str
    assignedUser: List[AssignedUser]


@dataclass
class SelfSelect:
    multiple: bool


@dataclass
class LeaderTop:
    endCondition: str
    endLevel: int


@dataclass
class Leader:
    level: int


@dataclass
class Refuse:
    type: str
    target: str


# 定义单个表单项的模型
class FormItem(BaseModel):
    custom_id: str = None
    name: str = None
    id: str = None
    type: str = None
    value: Any = None
    printable: bool = True
    required: bool = False


class Props(BaseModel):
    assignedUser: List[AssignedUser] = []
    formPerms: List[FormPerm] = []
    assignedType: Optional[str] = None
    mode: Optional[str] = None
    # sign: Optional[bool] = None
    # nobody: Optional[Nobody] = None
    # timeLimit: Optional[TimeLimit] = None
    # selfSelect: Optional[SelfSelect] = None
    # leaderTop: Optional[LeaderTop] = None
    # leader: Optional[Leader] = None
    # role: List[str] = field(default_factory=list)
    # refuse: Optional[Refuse] = None
    formUser: str = None


NodeDefinition = ForwardRef("NodeDefinition")


class NodeDefinition(BaseModel):
    id: Optional[str] = None
    parentId: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    props: Optional[Props] = Props()
    children: NodeDefinition = None  # 嵌套的子节点

    @classmethod
    def get_process_node_by_node_id(cls, node, node_id: str):
        while node.children and node.id != node_id:
            node = node.children
        if node.id == node_id:
            return node
        return None

    @classmethod
    def get_process_node_list(cls, node):
        nodes = []
        if not node.id:
            return nodes
        while node.children and node.children.id:
            node = node.children
            nodes.append(node)
        return nodes


NodeDefinition.update_forward_refs()


class ProcessDefinition(BaseModel):
    processDefinitionId: Optional[str] = None
    # 审批摸板ID
    templateId: str
    # 表单相关字段
    formId: str
    formName: str
    # 摸板名称
    templateName: str
    groupId: int
    # 摸板表单json str
    formItems: List[FormItem]
    # settings: str
    process: NodeDefinition = None
    # 权限字段
    whoCommit: List[str]
    whoEdit: List[str]
    whoExport: List[str]
    # 备注字段
    remark: str
    # 状态字段
    isStop: bool
    # 时间戳字段
    created: datetime
    updated: datetime

    @root_validator(pre=True)
    def parse_all_json_strings(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        parsed_values = {}
        for key, val in values.items():
            if isinstance(val, str):
                try:
                    parsed_values[key] = json.loads(val)  # 尝试解析字符串
                except json.JSONDecodeError:
                    parsed_values[key] = val  # 如果解析失败，则保持原值
            else:
                parsed_values[key] = val  # 非字符串直接保留
        return parsed_values
