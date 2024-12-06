from enum import Enum

URL_CAMUNDA_ENGINE = "http://10.129.133.160:9999/engine-rest"
URL_BPM_DEFINE = "http://10.129.133.160:9999/bpm-engine/process/definition/{definitionKey}"
URL_BPM_DELETE_INSTANCE = "http://10.129.133.160:9999/bpm-engine/process/instance/{id}"

FORM_VAR = "formData"
PROCESS_STATUS = "processStatus"
START_USER_INFO = "startUser"
APPLY_USER_ID = "applyUserId"
TASK_STATUS = "taskStatus"
NODE_SUFFIX = "#multiInstanceBody"


class FormPermType(Enum):
    READ = "R"
    EDITABLE = "E"
    HIDDEN = "H"


class UserType(Enum):
    user = "user"
    department = "dept"


class AssigneeType(Enum):
    ASSIGN_USER = "ASSIGN_USER"
    SELF_SELECT = "SELF_SELECT"
    LEADER_TOP = "LEADER_TOP"
    LEADER = "LEADER"
    ROLE = "ROLE"
    SELF = "SELF"
    FORM_USER = "FORM_USER"


class BpmDeleteReason(Enum):
    COMPLETED = "completed"  # 已完成
    DELETED = "deleted"


class BpmInstanceStatus(Enum):
    ACTIVE = "ACTIVE"  # 处理中
    REJECTED = "REJECTED"  # 驳回
    CANCELED = "CANCELED"  # 撤销
    PENDING = "PENDING"  # 正在处理
    COMPLETED = "COMPLETED"  # 已完成
    EXTERNALLY_TERMINATED = "EXTERNALLY_TERMINATED"  # 已终止


class ApprovalTaskStatus(Enum):
    PENDING = "PENDING"  # 审批中
    APPROVED = "APPROVED"  # 通过
    REJECTED = "REJECTED"  # 拒绝
    # TRANSFERRED = "TRANSFERRED"  # 已转交
    DONE = "DONE"  # 完成
    # REVERTED = "REVERTED"  # 已还原
    # ROLLBACK = "ROLLBACK"  # 已退回
    CANCELED = "CANCELED"


class ApprovalTimeLineEventType(Enum):
    START = "START"  # 审批开始
    PASS = "PASS"  # 通过
    REJECT = "REJECT"  # 拒绝
    # AUTO_PASS = "AUTO_PASS"  # 自动通过
    # AUTO_REJECT = "AUTO_REJECT"  # 自动拒绝
    # REMOVE_REPEAT = "REMOVE_REPEAT"  # 去重
    # TRANSFER = "TRANSFER"  # 转交
    # ADD_APPROVER_BEFORE = "ADD_APPROVER_BEFORE"  # 前加签
    # ADD_APPROVER = "ADD_APPROVER"  # 并加签
    # ADD_APPROVER_AFTER = "ADD_APPROVER_AFTER"  # 后加签
    # DELETE_APPROVER = "DELETE_APPROVER"  # 减签
    # ROLLBACK_SELECTED = "ROLLBACK_SELECTED"  # 指定回退
    # ROLLBACK = "ROLLBACK"  # 全部回退
    CANCEL = "CANCEL"  # 撤回
    DELETE = "DELETE"  # 删除
    # CC = "CC"  # 抄送


class ApprovalInstanceStatus(Enum):

    # INIT = "INIT"  # 平台初始化，提交创建审批异步任务后，推送【INIT】状态
    # PREPROCESS = "PREPROCESS"  # 平台处理中，审批创建异步任务处理中，推送【PREPROCESS】状态
    # CREATED = "CREATED"  # 审批创建完成，审批创建异步任务完成，推送【CREATED】状态
    # INNER_PROCESSING = "INNER_PROCESSING"  # 内部处理中，审批实例处理中（飞书处理中），推送【INNER_PROCESSING】状态

    PENDING = "PENDING"  # 用户创建审批后，推送【PENDING】状态
    APPROVED = "APPROVED"  # 任一审批人拒绝后，推送【REJECTED】状态
    REJECTED = "REJECTED"  # 流程中所有人同意后，推送【APPROVED】状态
    CANCELED = "CANCELED"  # 发起人撤回审批后，推送【CANCELED】状态
    # DELETED = "DELETED"  # 已删除: 审批定义被管理员删除后
    # REVERTED = "REVERTED"  # 已撤销: 发起人撤销已通过的审批
    # OVERTIME_CLOSE = "OVERTIME_CLOSE"  # 超时被关闭: 审批实例超时未处理被关闭
    # OVERTIME_RECOVER = "OVERTIME_RECOVER"  # 超时实例被恢复: 已超时的审批实例手动恢复
