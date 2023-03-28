from datetime import datetime
from typing import List


class ConverterData:

    @staticmethod
    def converter_data_json(data):
        json_response = dict()
        if data:
            for key, value in data.__dict__.items():
                if key == '_sa_instance_state':
                    continue
                json_response[key] = value
                if isinstance(value, datetime):
                    json_response[key] = str(value)
        return json_response
    @staticmethod
    def data_to_json_list(list_data: List) -> list:
        list_response = list()
        for data in list_data:
            list_response.append(ConverterData.converter_data_json(data=data).copy())
        return list_response
