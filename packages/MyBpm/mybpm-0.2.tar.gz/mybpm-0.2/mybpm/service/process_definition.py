import json

import requests
from mybpm.constant import URL_BPM_DEFINE, URL_BPM_DELETE_INSTANCE
from mybpm.model.definition import ProcessDefinition
from mybpm.utils.form_util import FormUtils


class BpmSystem:
    @classmethod
    def get_process_definition(cls, definition_code):
        req_url = URL_BPM_DEFINE.format(definitionKey=definition_code)
        response = requests.get(req_url)

        if response.status_code == 200:
            response_data = response.json()
            form_items_str = response_data.get("formItems", "[]")
            form_items = json.loads(form_items_str)
            if form_items:
                transformed_form_items = FormUtils.transfer_to_lark_form_item(form_items)
                response_data["formItems"] = transformed_form_items
            processDefinition = ProcessDefinition(**response_data)
            return processDefinition
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return None

    @classmethod
    def delete_process_instance(cls, instance_id):
        req_url = URL_BPM_DELETE_INSTANCE.format(id=instance_id)
        response = requests.delete(req_url)

        if response.status_code == 200:
            data = response.json()

            return data
        print(f"Request failed with status code {response.status_code}: {response.text}")
        return None


# ans = get_process_definition_form("1846798945182056448")
