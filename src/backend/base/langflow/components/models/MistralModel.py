from langchain_mistralai import ChatMistralAI
from pydantic.v1 import SecretStr

from langflow.base.constants import STREAM_INFO_TEXT
from langflow.base.models.model import LCModelComponent
from langflow.field_typing import LanguageModel
from langflow.io import BoolInput, DropdownInput, FloatInput, IntInput, MessageInput, Output, SecretStrInput, StrInput


class MistralAIModelComponent(LCModelComponent):
    display_name = "MistralAI"
    description = "Generates text using MistralAI LLMs."
    icon = "MistralAI"

    inputs = [
        MessageInput(name="input_value", display_name="Input"),
        IntInput(
            name="max_tokens",
            display_name="Max Tokens",
            advanced=True,
            info="The maximum number of tokens to generate. Set to 0 for unlimited tokens.",
        ),
        DropdownInput(
            name="model_name",
            display_name="Model Name",
            advanced=False,
            options=[
                "open-mixtral-8x7b",
                "open-mixtral-8x22b",
                "mistral-small-latest",
                "mistral-medium-latest",
                "mistral-large-latest",
                "codestral-latest",
            ],
            value="codestral-latest",
        ),
        StrInput(
            name="mistral_api_base",
            display_name="Mistral API Base",
            advanced=True,
            info=(
                "The base URL of the Mistral API. Defaults to https://api.mistral.ai/v1. "
                "You can change this to use other APIs like JinaChat, LocalAI and Prem."
            ),
        ),
        SecretStrInput(
            name="mistral_api_key",
            display_name="Mistral API Key",
            info="The Mistral API Key to use for the Mistral model.",
            advanced=False,
        ),
        FloatInput(name="temperature", display_name="Temperature", advanced=False, value=0.1),
        BoolInput(name="stream", display_name="Stream", info=STREAM_INFO_TEXT, advanced=True),
        StrInput(
            name="system_message",
            display_name="System Message",
            info="System message to pass to the model.",
            advanced=True,
        ),
        IntInput(name="max_retries", display_name="Max Retries", advanced=True),
        IntInput(name="timeout", display_name="Timeout", advanced=True),
        IntInput(name="max_concurrent_requests", display_name="Max Concurrent Requests", advanced=True),
        FloatInput(name="top_p", display_name="Top P", advanced=True),
        IntInput(name="random_seed", display_name="Random Seed", value=1, advanced=True),
        BoolInput(name="safe_mode", display_name="Safe Mode", advanced=True),
    ]

    outputs = [
        Output(display_name="Text", name="text_output", method="text_response"),
        Output(display_name="Language Model", name="model_output", method="build_model"),
    ]

    def build_model(self) -> LanguageModel:
        mistral_api_key = self.mistral_api_key
        temperature = self.temperature
        model_name = self.model_name
        max_tokens = self.max_tokens
        mistral_api_base = self.mistral_api_base or "https://api.mistral.ai/v1"
        max_retries = self.max_retries
        timeout = self.timeout
        max_concurrent_requests = self.max_concurrent_requests
        top_p = self.top_p
        random_seed = self.random_seed
        safe_mode = self.safe_mode

        if mistral_api_key:
            api_key = SecretStr(mistral_api_key)
        else:
            api_key = None

        output = ChatMistralAI(
            max_tokens=max_tokens or None,
            model_name=model_name,
            endpoint=mistral_api_base,
            api_key=api_key,
            temperature=temperature,
            max_retries=max_retries,
            timeout=timeout,
            max_concurrent_requests=max_concurrent_requests,
            top_p=top_p,
            random_seed=random_seed,
            safe_mode=safe_mode,
        )

        return output
