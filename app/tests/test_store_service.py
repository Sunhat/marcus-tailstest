import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.store_service import StoreService
from app.infra.persistence.json_store_repository import JsonStoreRepository
from app.schemas.store import Store


@pytest.fixture
def mock_repo():
    repo = MagicMock(spec=JsonStoreRepository)
    repo.get_all_enriched.return_value = [
        Store(name="A North", postcode="ZE1", latitude=56.15, longitude=-3.4),
        Store(name="B Central", postcode="EH1", latitude=55.95, longitude=-3.35),
        Store(name="C South", postcode="TR27", latitude=54.12, longitude=-3.52),
    ]
    return repo


@pytest.mark.asyncio
async def test_search_nearby_north_to_south_ordering(mock_repo):
    service = StoreService(mock_repo)

    mock_api = AsyncMock()
    mock_api.lookup = AsyncMock(return_value={
        "latitude": 55.95,
        "longitude": -3.40,
        "postcode": "EH1 1AA",
    })

    with patch("app.services.store_service.PostcodesIO") as MockClass:
        mock_instance = AsyncMock()
        mock_instance.__aenter__.return_value = mock_api
        mock_instance.__aexit__.return_value = None
        mock_instance.lookup = mock_api.lookup

        MockClass.return_value = mock_instance

        results = await service.search_nearby("EH1 1AA", radius_km=4000)

    assert len(results) == 3
    assert results[0].name == "A North"
    assert results[1].name == "B Central"
    assert results[2].name == "C South"


@pytest.mark.asyncio
async def test_search_nearby_filters_by_radius(mock_repo):
    service = StoreService(mock_repo)

    mock_api = AsyncMock()
    mock_api.lookup = AsyncMock(return_value={
        "latitude": 55.95,
        "longitude": -3.35,
    })

    with patch("app.services.store_service.PostcodesIO") as MockClass:
        mock_instance = AsyncMock()
        mock_instance.__aenter__.return_value = mock_api
        mock_instance.__aexit__.return_value = None

        MockClass.return_value = mock_instance

        results = await service.search_nearby("EH1 1AA", radius_km=5)

    assert len(results) == 1
    assert results[0].name == "B Central"


@pytest.mark.asyncio
async def test_search_nearby_handles_invalid_postcode(mock_repo):
    service = StoreService(mock_repo)

    mock_api = AsyncMock()
    mock_api.lookup = AsyncMock(return_value=None)

    with patch("app.services.store_service.PostcodesIO") as MockClass:
        mock_instance = AsyncMock()
        mock_instance.__aenter__.return_value = mock_api
        mock_instance.__aexit__.return_value = None

        MockClass.return_value = mock_instance

        results = await service.search_nearby("INVALID", radius_km=10)

    assert results == []


@pytest.mark.asyncio
async def test_search_nearby_handles_missing_coords(mock_repo):
    service = StoreService(mock_repo)

    mock_api = AsyncMock()
    mock_api.lookup = AsyncMock(return_value={"status": 200, "postcode": "EH1 1AA"})

    with patch("app.services.store_service.PostcodesIO") as MockClass:
        mock_instance = AsyncMock()
        mock_instance.__aenter__.return_value = mock_api
        mock_instance.__aexit__.return_value = None

        MockClass.return_value = mock_instance

        results = await service.search_nearby("EH1 1AA", radius_km=10)

    assert results == []
