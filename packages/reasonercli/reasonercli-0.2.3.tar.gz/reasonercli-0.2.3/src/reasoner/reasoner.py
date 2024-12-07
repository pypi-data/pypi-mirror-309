from typing import Optional
import httpx

from .config import read_config_file

BASE_URL = "https://api.reasoner.sh"
REASONER_SDK = "reasoner-1-pro"


def try_get_api_key_from_config_file():
    try:
        config = read_config_file()
        api_key = config.get("API_KEY")
        return api_key
    except Exception:
        pass


class Reasoner:
    def __init__(self, api_key: Optional[str] = None, base_url=BASE_URL):
        self.client = None
        self.base_url = base_url

        if api_key:
            self.api_key = api_key
        else:
            self.api_key = try_get_api_key_from_config_file()

        if not self.api_key:
            raise KeyError(
                "API key was not set. It must be set in ~/.reasoner/config or passed into Reasoner(api_key)"
            )

        self.client = httpx.Client(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "X-REASONER-SDK": REASONER_SDK,
            },
            timeout=300.0,
        )

    def close(self):
        if self.client:
            self.client.close()
            self.client = None

    @property
    def auth(self):
        from .auth import Auth

        return Auth(self.client, self.base_url)

    @property
    def documents(self):
        from .documents import Documents

        return Documents(self.client, self.base_url)

    @property
    def batches(self):
        from .batches import Batches

        return Batches(self.client, self.base_url)

    @property
    def chat(self):
        from .chat import Chat

        return Chat(self.client, self.base_url)


class ReasonerAsync:
    def __init__(self, api_key: Optional[str] = None, base_url=BASE_URL):
        self.api_key = api_key
        self.client = None
        self.base_url = base_url

        if api_key:
            self.api_key = api_key
        else:
            self.api_key = try_get_api_key_from_config_file()

        if not self.api_key:
            raise KeyError(
                "API key was not set. It must be set in ~/.reasoner/config or passed into ReasonerAsync(api_key)"
            )

        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "X-REASONER-SDK": REASONER_SDK,
            },
            timeout=300.0,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        if self.client:
            await self.client.aclose()
            self.client = None

    @property
    def auth(self):
        from .auth import AuthAsync

        return AuthAsync(self.client, self.base_url)

    @property
    def documents(self):
        from .documents import DocumentsAsync

        return DocumentsAsync(self.client, self.base_url)

    @property
    def batches(self):
        from .batches import BatchesAsync

        return BatchesAsync(self.client, self.base_url)

    @property
    def chat(self):
        from .chat import ChatAsync

        return ChatAsync(self.client, self.base_url)
