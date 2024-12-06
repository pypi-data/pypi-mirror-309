import json


class FormUtils:
    # 初始化映射
    to_lark_form_type = {
        "TextInput": "input",
        "TextareaInput": "textarea",
        "UserPicker": "contact",
        "DateTime": "date",
        "SelectInput": "radioV2",
        "FileUpload": "attachmentV2",
    }

    @classmethod
    def process_select(cls, source_object, result_object):
        options = source_object.get("props", {}).get("options", [])
        transformed_options = []
        for option in options:
            transformed_options.append({"value": option, "text": option})  # 动态生成唯一值  # 原始选项作为文本
        result_object["option"] = transformed_options

    @classmethod
    def process_file_upload(cls, source_object, result_object):
        pass

    @classmethod
    def process_datetime(cls, source_object, result_object):
        result_object["value"] = source_object.get("value")

    # 映射类型到对应的类方法
    extra_process_type = {
        "select": process_select,
        "file_upload": process_file_upload,
        "datetime": process_datetime,
    }

    @classmethod
    def extra_process(cls, source_object, result_object):
        item_type = result_object.get("type")
        # 如果类型不在映射表中，直接返回 None 或跳过
        if item_type not in cls.extra_process_type:
            return None
        # 调用映射的方法
        return cls.extra_process_type[item_type](cls, source_object, result_object)

    @classmethod
    def transfer_to_lark_form_item(cls, form_items: list) -> list:
        result_array = []

        for source_object in form_items:
            result_object = {}
            result_object["id"] = source_object.get("id")
            result_object["custom_id"] = source_object.get("customId")
            result_object["name"] = source_object.get("title")
            result_object["type"] = FormUtils.to_lark_form_type.get(source_object.get("name"), "")

            # 处理 props
            props_object = source_object.get("props", {})
            result_object["printable"] = props_object.get("enablePrint", False)
            result_object["required"] = props_object.get("required", False)
            FormUtils.extra_process(source_object, result_object)
            result_array.append(result_object)

        return result_array
