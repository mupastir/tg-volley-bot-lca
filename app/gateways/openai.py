import httpx
from typing import Optional, List, Type, TypeVar
from pydantic import BaseModel
from copy import deepcopy

from app.models.openai.response import Answer
from app.models.openai.request import Message

OAI_V1 = "https://api.openai.com/v1/"

T = TypeVar("T", bound=BaseModel)


class OpenAIError(Exception):
    pass


class OpenAI:
    def __init__(
        self,
        api_key: str,
        organization: Optional[str] = None,
        model: str = "gpt-4o-mini",
    ):
        self._model = model
        self._auth_header = deepcopy(
            {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        )
        if organization:
            self._auth_header["OpenAI-Organization"] = organization
        self._api_key = api_key

    async def call(self, endpoint: str, return_type: Type[T], payload: dict = {}) -> T:
        url = OAI_V1 + endpoint
        headers = self._auth_header
        async with httpx.AsyncClient(timeout=180) as client:
            response = await client.post(url, headers=headers, json=payload)
            if response.status_code != 200:
                raise OpenAIError(f"Error: {response.status_code} - {response.text}")
            js = response.json()
            return return_type.model_validate(js)

    async def complete(
        self,
        messages: List[Message],
        max_tokens: Optional[int] = None,
        presence_penalty: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        json: Optional[bool] = None,
        temperature: Optional[float] = None,
        **payload: bool,
    ) -> Answer:
        model: str = self._model
        req = {}

        params = locals()
        for opt in [
            "model",
            "max_tokens",
            "presence_penalty",
            "frequency_penalty",
            "temperature",
        ]:
            if opt in params and params[opt] is not None:
                req[opt] = params[opt]

        if json:
            req["response_format"] = {"type": "json_object"}

        req_messages = []
        for msg in messages:
            req_messages.append(msg.model_dump())

        req["messages"] = req_messages
        response = await self.call("chat/completions", Answer, req)
        return response

    async def easy_complete(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs: bool
    ) -> str:
        if system_prompt:
            messages = [
                Message(role="system", content=system_prompt),
                Message(role="user", content=prompt),
            ]
        else:
            messages = [Message(role="user", content=prompt)]
        answer = await self.complete(messages, **kwargs)
        if not answer.choices:
            raise OpenAIError("No response from OpenAI")
        return answer.choices[0].message.content
