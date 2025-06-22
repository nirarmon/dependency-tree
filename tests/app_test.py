import pytest
from app import app, NPMDependenciesTree, InMemoryCache, HtmlTreeRenderer, NPMRegistryClient


def setup_module(module):
    # create minimal tree object for the flask app
    app.tree = NPMDependenciesTree(NPMRegistryClient('mock'), InMemoryCache(), HtmlTreeRenderer())

def test_default_route_contains_search_form():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "<form action='/packages' method='get'" in html
    assert "name='package'" in html

def test_renderer_includes_search_form():
    renderer = HtmlTreeRenderer()
    renderer.add_new_entry('pkg:1.0.0', 0)
    html = renderer.render()
    assert "<form action='/packages' method='get'" in html
    assert "<div id='tree'>" in html
