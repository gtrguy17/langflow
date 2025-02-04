from typing import Union

from langflow.custom import CustomComponent
from langflow.field_typing import Text
from langflow.schema import Data


class PassComponent(CustomComponent):
    display_name = "Pass"
    description = "A pass-through component that forwards the second input while ignoring the first, used for controlling workflow direction."
    field_order = ["ignored_input", "forwarded_input"]

    def build_config(self) -> dict:
        return {
            "ignored_input": {
                "display_name": "Ignored Input",
                "info": "This input is ignored. It's used to control the flow in the graph.",
                "input_types": ["Text", "Data"],
            },
            "forwarded_input": {
                "display_name": "Input",
                "info": "This input is forwarded by the component.",
                "input_types": ["Text", "Data"],
            },
        }

    def build(self, ignored_input: Text, forwarded_input: Text) -> Union[Text, Data]:
        # The ignored_input is not used in the logic, it's just there for graph flow control
        self.status = forwarded_input
        return forwarded_input
