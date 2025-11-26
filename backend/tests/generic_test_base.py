from typing import Type
from fastapi.testclient import TestClient
from polyfactory.factories.pydantic_factory import ModelFactory

class CRUDApiTestBase:
    """
    Base class for automatic CRUD testing.
    Inherit from this and set the class attributes to get free tests.
    """
    url_prefix: str = ""
    create_factory: Type[ModelFactory] = None
    update_factory: Type[ModelFactory] = None

    def test_create_item(self, client: TestClient):
        # 1. Generate valid random data
        data = self.create_factory.build()
        payload = data.model_dump(mode='json')

        # 2. POST to the API
        response = client.post(f"{self.url_prefix}/", json=payload)
        
        # 3. Assert success and data match
        assert response.status_code == 201
        content = response.json()
        assert "id" in content
        # Check that sent fields match received fields
        for key, value in payload.items():
            assert content[key] == value

    def test_read_list(self, client: TestClient):
        # Create an item first so the list isn't empty
        data = self.create_factory.build()
        client.post(f"{self.url_prefix}/", json=data.model_dump(mode='json'))

        response = client.get(f"{self.url_prefix}/")
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_read_one(self, client: TestClient):
        # 1. Create item
        data = self.create_factory.build()
        create_res = client.post(f"{self.url_prefix}/", json=data.model_dump(mode='json'))
        item_id = create_res.json()["id"]

        # 2. Get item
        response = client.get(f"{self.url_prefix}/{item_id}")
        assert response.status_code == 200
        assert response.json()["id"] == item_id

    def test_update_item(self, client: TestClient):
        # 1. Create item
        data = self.create_factory.build()
        create_res = client.post(f"{self.url_prefix}/", json=data.model_dump(mode='json'))
        item_id = create_res.json()["id"]

        # 2. Generate update data
        update_data = self.update_factory.build()
        payload = update_data.model_dump(mode='json', exclude_unset=True)

        # 3. PUT item
        response = client.put(f"{self.url_prefix}/{item_id}", json=payload)
        assert response.status_code == 200
        
        # 4. Verify update
        content = response.json()
        for key, value in payload.items():
            assert content[key] == value

    def test_delete_item(self, client: TestClient):
        # 1. Create item
        data = self.create_factory.build()
        create_res = client.post(f"{self.url_prefix}/", json=data.model_dump(mode='json'))
        item_id = create_res.json()["id"]

        # 2. Delete item
        del_res = client.delete(f"{self.url_prefix}/{item_id}")
        assert del_res.status_code == 200

        # 3. Verify it's gone
        get_res = client.get(f"{self.url_prefix}/{item_id}")
        assert get_res.status_code == 404