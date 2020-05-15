import json

import pytest


@pytest.fixture
def manifesto_item_fill(admin_client):
    with open("test_data.txt", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        admin_client.post("/manifesto_item/", data=item)
    return admin_client
