from app import app, NPMDependenciesTree
import json
from unittest.mock import MagicMock


def test_default_route_serves_react_app():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert '<div id="root"></div>' in html


def test_packages_route_returns_json(monkeypatch):
    client = app.test_client()

    mock_tree_data = {"name": "react", "children": []}

    mock_build = MagicMock()
    mock_get = MagicMock(return_value=json.dumps(mock_tree_data))

    monkeypatch.setattr(NPMDependenciesTree, "build_dependencies_tree", mock_build)
    monkeypatch.setattr(NPMDependenciesTree, "get_dependencies_tree", mock_get)

    response = client.get("/packages?package=react&version=latest")

    assert response.status_code == 200
    assert response.mimetype == 'application/json'
    assert response.get_json() == mock_tree_data
