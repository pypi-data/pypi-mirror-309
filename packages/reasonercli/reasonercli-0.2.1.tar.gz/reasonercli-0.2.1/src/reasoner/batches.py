class Batches:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    def get_status(self, batch_uid: str):
        response = self.client.get(f'{self.base_url}/public/v1/batches/{batch_uid}')
        response.raise_for_status()

        response_json = response.json() or {}
        return response_json.get("batch", {}).get("status")


class BatchesAsync:
    def __init__(self, client, base_url):
        self.client = client
        self.base_url = base_url

    async def get_status(self, batch_uid: str):
        response = await self.client.get(f'{self.base_url}/public/v1/batches/{batch_uid}')
        response.raise_for_status()

        response_json = response.json() or {}
        return response_json.get("batch", {}).get("status")
