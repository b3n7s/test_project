import pytest

from services.agrohelper_client import auth_as_admin


@pytest.fixture(scope="session")
def client():
    """Создаем авторизованный клиент для всех тестов"""
    return auth_as_admin()


def test_get_farmers(client):
    """Тест получения списка фермеров"""
    response = client.get(
        "/api/farmers", params={"page": 1, "limit": 10, "pagination": "true"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)


def test_get_admin_users_agents(client):
    """Тест получения агентов"""
    response = client.get("/api/admin/users/agents")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_admin_users_organizers(client):
    """Тест получения организаций"""
    response = client.get("/api/admin/users/organizers")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_qualities(client):
    """Тест получения качества"""
    response = client.get("/api/qualities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_regions(client):
    """Тест получения регионов"""
    response = client.get("/api/regions")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_cultures(client):
    """Тест получения культур"""
    response = client.get("/api/cultures")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_user_me(client):
    """Тест получения информации о пользователе"""
    response = client.get("/api/user/me")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_tariffs(client):
    """Тест получения тарифов с фильтрами"""
    response = client.get(
        "/api/tariffs",
        params={"page": "1", "limit": "10", "order[from]": ""},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_regions_with_filters(client):
    """Тест получения регионов с фильтрами"""
    response = client.get("/api/regions", params={"page": "1", "limit": "10"})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_calls_with_filters(client):
    """Тест получения истории звонков с фильтрами"""
    response = client.get(
        "/api/calls", params={"page": "1", "limit": "10", "pagination": "true"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_farmers_with_filters(client):
    response = client.get(
        "/api/farmers",
        params={"page": "1", "limit": "10", "pagination": "true"},
    )
    assert response.status_code == 200


def test_get_v0_calls_admin_scenarios(client):
    response = client.get("/api/v0/calls/admin/scenarios")
    assert response.status_code == 200


def test_get_calls_dictionary_price(client):
    response = client.get("/api/calls/dictionary/price")
    assert response.status_code == 200


def test_get_farmer_profile(client):
    response = client.get("/api/farmers/67c26da7-1133-4fc3-be72-f2f020b5b6fb")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_inner_profile(client):
    response = client.get("/api/user/6f692f34-e6ee-4b0b-8cad-04ec40e151a5")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_warehouses_by_owner(client):
    response = client.get(
        "/api/warehouses",
        params={
            "filter[owner]": "67c26da7-1133-4fc3-be72-f2f020b5b6fb",
            "page": "1",
            "limit": "10",
            "pagination": "true",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_offers_by_farmer(client):
    response = client.get(
        "/api/offers",
        params={
            "filter[farmer]": "67c26da7-1133-4fc3-be72-f2f020b5b6fb",
            "page": "1",
            "limit": "10",
            "pagination": "true",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_farmers_phonecalls(client):
    response = client.get(
        "/api/farmers/67c26da7-1133-4fc3-be72-f2f020b5b6fb/phonecalls",
        params={
            "page": "1",
            "limit": "10",
            "pagination": "true",
            "order": "desc",
            "callmethod": "new",
        },
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
