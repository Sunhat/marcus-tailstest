import json
from pathlib import Path
from typing import List
from app.config import get_settings
from app.infra.external.postcodes_io import PostcodesIO
from app.schemas.store import OrderDirection, Store

class JsonStoreRepository:
    def __init__(self, settings = get_settings()):
        self.settings = settings
        self.store_file: Path = settings.stores_file
        self.enriched_file: Path = settings.enriched_stores_file

    def get_all_enriched(self) -> List[Store]:
        if not self.enriched_file.is_file():
            return []

        try:
            with self.enriched_file.open(encoding="utf-8") as f:
                data = json.load(f)
            return [Store.model_validate(s) for s in data]
        except Exception as e:
            print(f"Failed to load enriched stores: {e}")
            return []

    async def enrich_if_needed(self) -> None:
        if self.enriched_file.is_file():
            return

        try:
            with self.store_file.open(encoding="utf-8") as f:
                raw = json.load(f)
            stores = [Store.model_validate(s) for s in raw]
        except Exception as e:
            print(f"Failed to load stores: {e}")
            return

        postcodes = [s.postcode.replace(" ", "").upper() for s in stores]

        async with PostcodesIO() as api:
            results = await api.bulk_lookup(postcodes)

        enriched = []
        for store in stores:
            pc = store.postcode.replace(" ", "").upper()
            if loc := results.get(pc):
                if loc.get("latitude") is not None and loc.get("longitude") is not None:
                    enriched.append(
                        Store(
                            **store.model_dump(),
                            latitude=loc["latitude"],
                            longitude=loc["longitude"],
                        )
                    )

        with self.enriched_file.open("w", encoding="utf-8") as f:
            json.dump([s.model_dump() for s in enriched], f, indent=2)
