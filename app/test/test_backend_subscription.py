import pytest
from conftest import client

def test_get_user_subscriptions_endpoint_empty(client):
    response = client.get("/subscriptions/", params={"user_tg_id": 123})
    assert response.status_code == 200
    # Если подписок нет, ожидается пустой список
    assert response.json() == []

def test_subscribe_endpoint_success(client):
    # Подписываем пользователя (tg_id=123) на жанр с id=1
    response = client.post("/subscribe/", json={"user_tg_id": 123, "genre_id": 1})
    assert response.status_code == 200
    assert response.json() == {"detail": "Subscribed"}

def test_subscribe_endpoint_already_subscribed(client):
    # Подписываем пользователя на жанр с id=2
    response = client.post("/subscribe/", json={"user_tg_id": 123, "genre_id": 2})
    assert response.status_code == 200
    # Повторная подписка на тот же жанр должна вернуть ошибку
    response = client.post("/subscribe/", json={"user_tg_id": 123, "genre_id": 2})
    assert response.status_code == 400
    assert response.json()["detail"] == "Already subscribed"

def test_unsubscribe_endpoint_success(client):
    # Сначала подписываем пользователя на жанр с id=3
    response = client.post("/subscribe/", json={"user_tg_id": 123, "genre_id": 3})
    assert response.status_code == 200
    # Затем отписываемся
    response = client.delete("/unsubscribe/", json={"user_tg_id": 123, "genre_id": 3})
    assert response.status_code == 200
    assert response.json() == {"detail": "Unsubscribed"}

def test_unsubscribe_endpoint_not_subscribed(client):
    response = client.delete("/unsubscribe/", json={"user_tg_id": 123, "genre_id": 999})
    assert response.status_code == 400
    assert response.json()["detail"] == "Not subscribed"