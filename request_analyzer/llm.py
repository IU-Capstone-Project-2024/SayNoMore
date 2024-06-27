import aiohttp


class LLM:

    def __init__(self, url: str = 'http://10.100.30.240:1222/generate') -> None:
        self.url = url

    async def get_response(self, json_data):
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=json_data) as response:
                if response.status != 200:
                    raise Exception(f"Error: {response.status}")
                return await response.json()
