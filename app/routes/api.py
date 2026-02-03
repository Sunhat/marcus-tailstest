from fastapi import APIRouter, Depends, Query
from app.schemas.store import StoresListQuery, StoresNearbyQuery, Store
from app.services.store_service import StoreService

router = APIRouter()


@router.get("/stores")
async def get_stores(
    query: StoresListQuery = Depends(),
    store_service: StoreService = Depends()
):
    return store_service.list(query.order)

@router.get("/stores/nearby", response_model=list[Store])
async def nearby_stores(
    query: StoresNearbyQuery = Depends(),
    store_service: StoreService = Depends(),
):
    nearby = await store_service.search_nearby(query.postcode, query.radius_km)
    if not nearby:
        raise HTTPException(status_code=404, detail="No stores found near this postcode or postcode invalid")
    return nearby
