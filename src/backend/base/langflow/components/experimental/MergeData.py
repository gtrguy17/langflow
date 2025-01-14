from langflow.custom import CustomComponent
from langflow.schema import Data


class MergeDataComponent(CustomComponent):
    display_name = "Merge Data"
    description = "Merges data."
    beta: bool = True

    field_config = {
        "data": {"display_name": "Data"},
    }

    def build(self, data: list[Data]) -> Data:
        if not data:
            return Data()
        if len(data) == 1:
            return data[0]
        merged_data = Data()
        for value in data:
            if merged_data is None:
                merged_data = value
            else:
                merged_data += value
        self.status = merged_data
        return merged_data


if __name__ == "__main__":
    data = [
        Data(data={"key1": "value1"}),
        Data(data={"key2": "value2"}),
    ]
    component = MergeDataComponent()
    result = component.build(data)
    print(result)
