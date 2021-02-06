from registry_client import NPMRegistryClient, PackageNotFoundExcetion, ServerErrorExcetion
import json
import pytest
from dependency_tree import NPMDependenciesTree
from dependency_tree import DependencyException

from cache_manager import InMemoryCache
from cache_manager import CacheException
from registry_client import NPMRegistryClient
from registry_client import PackageNotFoundExcetion
from registry_client import ServerErrorExcetion
from dependency_tree_renderer import HtmlTreeRenderer
from dependency_tree_renderer import RendererException

def dependencies_response(self,package,version):
    if package == 'accepts':
        return json.loads('{\"name\":\"accepts\",\"version\":\"1.0.2\"}')
    if package == 'array-flatten':
        return json.loads('{\"name\":\"array-flatten\",\"version\":\"1.0.2\"}')
    if package == 'express':
        return json.loads('{\"name\":\"express\",\"version\":\"4.17.1\",\"dependencies\":{\"accepts\": \"~1.3.7\",\"array-flatten\": \"1.1.1\"}}')

def mock_package_not_found_exception(self,package,version):
    raise PackageNotFoundExcetion('some_package','1.0.0')

def mock_server_error_exception(self,package,version):
    raise ServerErrorExcetion('some_package','1.0.0')

def mock_cache_error_exception(self,package,version):
    raise CacheException('some_package','1.0.0')

@pytest.fixture
def mock_with_no_dependencies(monkeypatch):
    from registry_client import NPMRegistryClient
    monkeypatch.setattr(NPMRegistryClient, "get_package_infromation", dependencies_response)

@pytest.fixture
def mock_with_with_dependencies(monkeypatch):
    from registry_client import NPMRegistryClient
    monkeypatch.setattr(NPMRegistryClient, "get_package_infromation", dependencies_response)

@pytest.fixture
def mock_package_not_found(monkeypatch):
    from registry_client import NPMRegistryClient
    monkeypatch.setattr(NPMRegistryClient, "get_package_infromation", mock_package_not_found_exception)

@pytest.fixture
def mock_server_error(monkeypatch):
    from cache_manager import InMemoryCache
    monkeypatch.setattr(InMemoryCache, "get_latest_version", mock_cache_error_exception)

@pytest.fixture
def mock_cache_error(monkeypatch):
    from registry_client import NPMRegistryClient
    monkeypatch.setattr(NPMRegistryClient, "get_package_infromation", mock_server_error_exception)

def test_build_tree_no_sub_dependencies_success(mock_with_no_dependencies,mocker):
    cache = InMemoryCache()
    mocker.spy(cache, 'add_package')
    tree_builder = NPMDependenciesTree(NPMRegistryClient('mock_address'),cache,HtmlTreeRenderer())
    response = tree_builder.build_dependencies_tree('accepts','latest')
    assert cache.add_package.call_count == 1

def test_build_tree_mock_package_not_found_no_exception(mock_package_not_found,mocker):
    client = NPMRegistryClient('mock_address')
    mocker.spy(client, 'get_package_infromation')
    tree_builder = NPMDependenciesTree(client,InMemoryCache(),HtmlTreeRenderer())
    response = tree_builder.build_dependencies_tree('some_package','latest')
    assert client.get_package_infromation.call_count == 1

def test_build_tree_mock_server_error_throws_exception(mock_server_error,mocker):
    with pytest.raises(Exception):
        client = NPMRegistryClient('mock_address')
        mocker.spy(client, 'get_package_infromation')
        tree_builder = NPMDependenciesTree(client,InMemoryCache(),HtmlTreeRenderer())
        response = tree_builder.build_dependencies_tree('some_package','latest')

def test_build_tree_cache_error_throws_exception(mock_cache_error,mocker):
    with pytest.raises(Exception):
        cache = InMemoryCache()
        tree_builder = NPMDependenciesTree(NPMRegistryClient('mock_address'),cache,HtmlTreeRenderer())
        response = tree_builder.build_dependencies_tree('some_package','latest')

def test_build_tree_with_sub_dependencies_success(mock_with_with_dependencies,mocker):
    cache = InMemoryCache()
    mocker.spy(cache, 'add_package')  
    tree_builder = NPMDependenciesTree(NPMRegistryClient('mock_address'),cache,HtmlTreeRenderer())
    response = tree_builder.build_dependencies_tree('express','latest')
    assert response is True
    assert cache.add_package.call_count == 4

def test_build_tree_with_sub_dependencies_success(mock_with_with_dependencies,mocker):
    cache = InMemoryCache()
    mocker.spy(cache, 'add_package')  
    tree_builder = NPMDependenciesTree(NPMRegistryClient('mock_address'),cache,HtmlTreeRenderer())
    response = tree_builder.build_dependencies_tree('express','latest')
    assert response is True
    assert cache.add_package.call_count == 4

def test_build_tree_package_already_in_cache(mock_with_with_dependencies,mocker):
    client = NPMRegistryClient('mock_address')
    mocker.spy(client, 'get_package_infromation')
    cache = InMemoryCache()
    cache.add_package('express','4.17.1')
    mocker.spy(cache, 'validate_package_exists')  
    tree_builder = NPMDependenciesTree(client,cache,HtmlTreeRenderer())
    response = tree_builder.build_dependencies_tree('express','4.17.1')
    assert response is True
    assert cache.validate_package_exists.call_count == 1
    assert client.get_package_infromation.call_count == 0