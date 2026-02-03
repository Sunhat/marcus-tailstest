from fastapi import APIRouter, Depends, Query
from pathlib import Path
import json
from typing import List, Dict, Literal, Optional
from app.schemas.store import OrderDirection
import httpx
from app.infra.external.postcodes_io import PostcodesIO
from app.infra.persistence.json_store_repository import JsonStoreRepository
from app.services.haversine import haversine
from app.schemas.store import Store


class StoreService:
    def __init__(self, repo: JsonStoreRepository = Depends()):
        self.repo = repo

    def list(self, order: Optional[OrderDirection] = None) -> List[Store]:
        stores = self.repo.get_all_enriched()
        if order:
            stores.sort(key=lambda s: s.name, reverse=order == "DESC")
        return stores
    async def search_nearby(
        self,
        postcode: str,
        radius_km: float = 10.0,
    ) -> List[Store]:
        stores = self.repo.get_all_enriched()
        if not stores:
            return []

        async with PostcodesIO() as api:
            coords = await api.lookup(postcode.replace(" ", "").upper())
            if not coords or coords.get("latitude") is None or coords.get("longitude") is None:
                return []

            origin_lat = coords["latitude"]
            origin_lon = coords["longitude"]

        def is_within_radius(store: Store) -> bool:
            dist = haversine(origin_lat, origin_lon, store.latitude, store.longitude)
            return dist <= radius_km

        within = [store for store in stores if is_within_radius(store)]

        within.sort(key=lambda s: s.latitude, reverse=True)

        return within
