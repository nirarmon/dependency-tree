from registry_client import (
    NPMRegistryClient,
    PackageNotFoundExcetion,
    ServerErrorExcetion,
)
import pytest
import requests


class MockResponse(object):
    def __init__(self, status_code, text=None):
        self.status_code = status_code
        self.text = text


@pytest.fixture
def mock_response_200(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(200, '{"name": "access", "version": "1.0.2"}')

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_response_404(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(404)

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_response_503(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(503)

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def client():
    return NPMRegistryClient("http://registry.npmjs.org/")


def test_get_information_package_not_exists_fail(client, mock_response_404):
    with pytest.raises(PackageNotFoundExcetion):
        client.get_package_infromation("packageNotExists", "1.1.1")


def test_get_information_sucsess(client, mock_response_200):
    response = client.get_package_infromation("access", "latest")
    assert response["name"] == "access"
    assert response is not None


def test_get_information_serverError(client, mock_response_503):
    with pytest.raises(ServerErrorExcetion):
        client.get_package_infromation("packageNotExists", "1.1.1")
