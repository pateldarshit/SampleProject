import json

import pytest
from django.test.client import Client
from rest_framework import status


def test_manifesto_item_view_get_success(manifesto_item_fill):
    response = manifesto_item_fill.get("/manifesto_item/")

    with open("test_data.txt", encoding="utf-8") as f:
        test_data = json.load(f)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == len(test_data)
    for index, item in enumerate(test_data):
        assert item["title"] == response.data[index]["title"]
        assert item["description"] == response.data[index]["description"]
        assert item["content_type"] == response.data[index]["content_type"]


def test_manifesto_item_view_get_id_success(manifesto_item_fill):
    test_item_ids = [1, 2, 3, 4]
    with open("test_data.txt", encoding="utf-8") as f:
        test_data = json.load(f)
    for item_id in test_item_ids:
        response = manifesto_item_fill.get(f"/manifesto_item/{item_id}/")

        assert response.status_code == status.HTTP_200_OK
        assert test_data[item_id - 1]["title"] == response.data["title"]
        assert test_data[item_id - 1]["description"] == response.data["description"]
        assert test_data[item_id - 1]["content_type"] == response.data["content_type"]


def test_manifesto_item_view_get_id_fail(manifesto_item_fill):
    test_item_id = 5
    response = manifesto_item_fill.get(f"/manifesto_item/{test_item_id}/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_manifesto_item_view_get_auth_fail():
    client = Client()
    response = client.get(f"/manifesto_item/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db(transaction=False)
def test_manifesto_item_view_post_success(manifesto_item_fill):
    new_item = {
        "title": "New item",
        "description": "Testing to add item",
        "content_type": "PRINCIPLE",
    }
    response = manifesto_item_fill.post(f"/manifesto_item/", data=new_item)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["id"] == 5
    assert response.data["owner"] == "admin"
    assert new_item["title"] == response.data["title"]
    assert new_item["description"] == response.data["description"]
    assert new_item["content_type"] == response.data["content_type"]


@pytest.mark.django_db(transaction=False)
def test_manifesto_item_view_post_fail(manifesto_item_fill):
    new_item = {
        "title": "New item",
        "description": "Testing to add item",
        "content_type": "XYZ",  # invalid content type
    }
    response = manifesto_item_fill.post(f"/manifesto_item/", data=new_item)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_manifesto_item_view_post_auth_fail():
    new_item = {
        "title": "New item",
        "description": "Testing to add item",
        "content_type": "XYZ",  # invalid content type
    }
    client = Client()
    response = client.post(f"/manifesto_item/", data=new_item)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db(transaction=False)
def test_manifesto_item_view_put_success(manifesto_item_fill):
    test_item_id = 2
    new_item = {
        "title": "New item",
        "description": "Testing to add item",
        "content_type": "VALUE",  # invalid content type
    }
    response = manifesto_item_fill.put(
        f"/manifesto_item/{test_item_id}/",
        data=new_item,
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == test_item_id
    assert response.data["owner"] == "admin"
    assert new_item["title"] == response.data["title"]
    assert new_item["description"] == response.data["description"]
    assert new_item["content_type"] == response.data["content_type"]


@pytest.mark.django_db(transaction=False)
def test_manifesto_item_view_put_fail(manifesto_item_fill):
    test_item_id = 2
    new_item = {
        "title": "New item",
        "description": "Testing to add item",
        "content_type": "XYZ",  # invalid content type
    }
    response = manifesto_item_fill.put(
        f"/manifesto_item/{test_item_id}/",
        data=new_item,
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=False)
def test_manifesto_item_view_put_not_found(manifesto_item_fill):
    test_item_id = 5
    new_item = {
        "title": "New item",
        "description": "Testing to add item",
        "content_type": "XYZ",  # invalid content type
    }
    response = manifesto_item_fill.put(
        f"/manifesto_item/{test_item_id}/",
        data=new_item,
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db(transaction=False)
def test_manifesto_item_view_put_auth_fail():
    test_item_id = 2
    new_item = {
        "title": "New item",
        "description": "Testing to add item",
        "content_type": "VALUE",  # invalid content type
    }
    client = Client()
    response = client.put(
        f"/manifesto_item/{test_item_id}/",
        data=new_item,
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db(transaction=False)
def test_manifesto_item_view_delete_success(manifesto_item_fill):
    test_item_id = 2
    response = manifesto_item_fill.delete(f"/manifesto_item/{test_item_id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db(transaction=False)
def test_manifesto_item_view_delete_success(manifesto_item_fill):
    test_item_id = 5
    response = manifesto_item_fill.delete(f"/manifesto_item/{test_item_id}/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db(transaction=False)
def test_manifesto_item_view_delete_success():
    test_item_id = 2
    client = Client()
    response = client.delete(f"/manifesto_item/{test_item_id}/")
    assert response.status_code == status.HTTP_403_FORBIDDEN
