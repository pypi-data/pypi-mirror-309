import httpx
import time

class Version:
    _base = 'https://whatexpsare.online/api/versions/current'

    @staticmethod
    def _current_time():
        return int(time.time() * 1000)

    async def get(self):
        _params = {"t": self._current_time()}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self._base, params=_params)
                response.raise_for_status()
                info = response.json()
                return {"Windows": info.get("Windows"), "Mac": info.get("Mac")}
            except httpx.RequestError as Error:
                print(f'Version - Error: {Error}')
                return None
