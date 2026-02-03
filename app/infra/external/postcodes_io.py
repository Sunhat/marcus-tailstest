import httpx
from typing import List, Dict, Optional

class PostcodesIO:
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url="https://api.postcodes.io",
            timeout=15.0,
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.aclose()

    async def bulk_lookup(self, postcodes: List[str]) -> Dict[str, Optional[Dict]]:
        resp = await self.client.post("/postcodes", json={"postcodes": postcodes})
        resp.raise_for_status()
        data = resp.json()
        return {
            item["query"]: item.get("result")
            for item in data["result"]
        }

    async def lookup(self, postcode: str) -> Dict[str, Optional[Dict]]:
        pc = postcode.replace(" ", "").upper()
        resp = await self.client.get(f"/postcodes/{pc}")

        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == 200:
                return data.get("result")

        return None
