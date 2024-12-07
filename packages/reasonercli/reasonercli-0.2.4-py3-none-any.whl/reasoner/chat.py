from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionResponse(BaseModel):
    response_uid: str


class Response(BaseModel):
    id: int
    uid: UUID
    status: str
    response: Dict[str, Any]
    api_key_id: int
    project_id: int
    is_answer: bool
    created_at: datetime
    updated_at: datetime


class Chat:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    def completion(
        self,
        messages: List[Message],
        batch_uid: Optional[str] = None,
        example_docs: Optional[str] = None,
    ):
        data = {"messages": messages}
        if batch_uid:
            data["batch_uid"] = batch_uid
        elif example_docs:
            data["example_docs"] = example_docs

        response = self.client.post(
            f"{self.base_url}/public/v1/chat/completion",
            json=data,
        )
        response.raise_for_status()
        return ChatCompletionResponse(**response.json())

    def get_response(self, response_uid: str):
        response = self.client.get(
            f"{self.base_url}/public/v1/chat/status/{response_uid}"
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return Response(**response.json())


class ChatAsync:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    async def completion(
        self,
        messages: List[Message],
        batch_uid: Optional[str] = None,
        example_docs: Optional[str] = None,
    ):
        data = {"messages": messages}
        if batch_uid:
            data["batch_uid"] = batch_uid
        elif example_docs:
            data["example_docs"] = example_docs

        response = await self.client.post(
            f"{self.base_url}/public/v1/chat/completion",
            json=data,
        )
        response.raise_for_status()
        return ChatCompletionResponse(**response.json())

    async def get_response(self, response_uid: str):
        response = await self.client.get(
            f"{self.base_url}/public/v1/chat/status/{response_uid}"
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return Response(**response.json())
