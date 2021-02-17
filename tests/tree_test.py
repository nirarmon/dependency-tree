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
    if package == 'statuses':
        return json.loads('{\"name\":\"statuses\",\"version\":\"1.0.5\"}')
    if package == 'accepts':
        return json.loads('{\"name\":\"accepts\",\"version\":\"1.0.2\",\"dependencies\":{\"statuses\": \"1.0.5\"}}')
    if package == 'array-flatten':
        return json.loads('{\"name\":\"array-flatten\",\"version\":\"1.0.2\"}')
    if package == 'express':
        return json.loads('{\"name\":\"express\",\"version\":\"4.17.1\",\"dependencies\":{\"accepts\": \"~1.3.7\",\"array-flatten\": \"1.1.1\"}}')
    if package == 'deprecated_package':
        return json.loads('{\"name\":\"express\",\"version\":\"4.17.1\",\"deprecated\":\"deprecated\"}')

def dependencies_response_with_circular_dependency(self,package,version):
    if package == 'statuses':
        return json.loads('{\"name\":\"statuses\",\"version\":\"1.0.5\"}')
    if package == 'accepts':
        return json.loads('{\"name\":\"accepts\",\"version\":\"1.0.2\",\"dependencies\":{\"express\": \"4.17.1\"}}')
    if package == 'array-flatten':
        return json.loads('{\"name\":\"array-flatten\",\"version\":\"1.0.2\"}')
    if package == 'express':
        return json.loads('{\"name\":\"express\",\"version\":\"4.17.1\",\"dependencies\":{\"accepts\": \"~1.3.7\",\"array-flatten\": \"1.1.1\"}}')
    if package == 'deprecated_package':
        return json.loads('{\"name\":\"express\",\"version\":\"4.17.1\",\"deprecated\":\"deprecated\"}')

def no_dependencies_response(self,package,version):
    if package == 'statuses':
        return json.loads('{\"name\":\"statuses\",\"version\":\"1.0.5\"}')

def mock_package_not_found_exception(self,package,version):
    raise PackageNotFoundExcetion('some_package','1.0.0')

def mock_server_error_exception(self,package,version):
    raise ServerErrorExcetion('some_package','1.0.0')

def mock_cache_error_exception(self,package,version):
    raise CacheException('some_package','1.0.0')

@pytest.fixture
def mock_with_no_dependencies(monkeypatch):
    from registry_client import NPMRegistryClient
    monkeypatch.setattr(NPMRegistryClient, "get_package_infromation", no_dependencies_response)

@pytest.fixture
def mock_with_with_dependencies(monkeypatch):
    from registry_client import NPMRegistryClient
    monkeypatch.setattr(NPMRegistryClient, "get_package_infromation", dependencies_response)

@pytest.fixture
def mock_with_with_circular_dependencies(monkeypatch):
    from registry_client import NPMRegistryClient
    monkeypatch.setattr(NPMRegistryClient, "get_package_infromation", dependencies_response_with_circular_dependency)


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
    response = tree_builder.build_dependencies_tree('statuses','latest')
    assert cache.add_package.call_count == 1

def test_build_tree_package_not_found_exception(mock_package_not_found,mocker):
    with pytest.raises(DependencyException) as exception:
        client = NPMRegistryClient('mock_address')
        mocker.spy(client, 'get_package_infromation')
        tree_builder = NPMDependenciesTree(client,InMemoryCache(),HtmlTreeRenderer())
        response = tree_builder.build_dependencies_tree('some_package','latest')
        assert client.get_package_infromation.call_count == 1
        assert exception.message == 'Could not find package: some_package:latest'

def test_build_tree_package_deprecated_exception(mock_package_not_found,mocker):
    with pytest.raises(DependencyException) as exception:
        client = NPMRegistryClient('mock_address')
        mocker.spy(client, 'get_package_infromation')
        tree_builder = NPMDependenciesTree(client,InMemoryCache(),HtmlTreeRenderer())
        response = tree_builder.build_dependencies_tree('deprecated_package','latest')
        assert client.get_package_infromation.call_count == 1
        assert exception.message == 'deprecated'

def test_build_tree_server_error_throws_exception(mock_server_error,mocker):
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

def test_update_latest_version_tree(mock_with_with_dependencies,mocker):
    client = NPMRegistryClient('mock_address')
    cache = InMemoryCache()
    cache.update_latest_version('express','4.17.0')
    mocker.spy(cache, 'update_latest_version')  
    tree_builder = NPMDependenciesTree(client,cache,HtmlTreeRenderer())
    mocker.spy(tree_builder,'build_dependencies_tree')
    response = tree_builder.update_latest_versions()
    cache.update_latest_version.assert_called_with('express','4.17.1')
    tree_builder.build_dependencies_tree.assert_called_with('express','latest')

def test_build_tree_with_circular_dependencies(mock_with_with_circular_dependencies,mocker):
    cache = InMemoryCache()
    mocker.spy(cache, 'add_package')
    tree_builder = NPMDependenciesTree(NPMRegistryClient('mock_address'),cache,HtmlTreeRenderer())
    response = tree_builder.build_dependencies_tree('express','latest')
    assert response==True
    response = tree_builder.get_dependencies_tree('express','latest')
    assert  response is not None