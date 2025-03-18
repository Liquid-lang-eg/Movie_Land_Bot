import urllib.parse
import pytest
from conftest import async_client

@pytest.mark.asyncio
async def test_recommend_movies_endpoint(async_client, monkeypatch):
    # Мокируем запрос к внешнему API TMDB для эндпоинта /movies/recommend
    class DummyResponse:
        status = 200
        async def json(self):
            return {"results": [
                {"title": "Movie 1", "release_date": "2020-01-01"},
                {"title": "Movie 2", "release_date": "2021-05-05"},
                {"title": "Movie 3", "release_date": "2019-07-07"},
                {"title": "Movie 4", "release_date": "2018-03-03"},
                {"title": "Movie 5", "release_date": "2022-09-09"},
                {"title": "Movie 6", "release_date": "2022-11-11"},
            ]}
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass

    class DummySession:
        async def get(self, url, params):
            return DummyResponse()
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass

    async def dummy_client_session(*args, **kwargs):
        return DummySession()

    monkeypatch.setattr("aiohttp.ClientSession", dummy_client_session)

    response = await async_client.get("/movies/recommend", params={"user_id": 123})
    assert response.status_code == 200
    data = response.json()
    assert "movies" in data
    assert isinstance(data["movies"], list)
    assert len(data["movies"]) == 5

@pytest.mark.asyncio
async def test_get_actor_movies_endpoint(async_client, monkeypatch):

    class DummySearchResponse:
        status = 200
        async def json(self):
            return {"results": [{"id": 100, "name": "Test Actor"}]}
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass

    class DummyCreditsResponse:
        status = 200
        async def json(self):
            return {"cast": [
                {"id": 1, "release_date": "2020-01-01"},
                {"id": 2, "release_date": "2021-01-01"},
            ]}
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass

    class DummySession:
        async def get(self, url, **kwargs):
            if "search" in url:
                return DummySearchResponse()
            elif "movie_credits" in url:
                return DummyCreditsResponse()
            return DummySearchResponse()
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass

    async def dummy_client_session(*args, **kwargs):
        return DummySession()

    monkeypatch.setattr("aiohttp.ClientSession", dummy_client_session)

    response = await async_client.get("/actors/movies/", params={"name": "Test Actor"})
    assert response.status_code == 200
    movies = response.json()
    assert isinstance(movies, list)
    if movies:
        for movie in movies:
            assert "tmdb_url" in movie

@pytest.mark.asyncio
async def test_search_movie_endpoint(async_client, monkeypatch):
    # Мокируем запрос для поиска фильма по названию
    class DummySearchResponse:
        status = 200
        async def json(self):
            return {"results": [{"id": 50, "title": "Found Movie", "release_date": "2020-01-01"}]}
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass

    class DummySession:
        async def get(self, url, **kwargs):
            return DummySearchResponse()
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc, tb):
            pass

    async def dummy_client_session(*args, **kwargs):
        return DummySession()

    monkeypatch.setattr("aiohttp.ClientSession", dummy_client_session)

    response = await async_client.get("/movies/search/", params={"title": "Found Movie"})
    assert response.status_code == 200
    movie = response.json()
    assert "tmdb_url" in movie
    assert movie["title"] == "Found Movie"
