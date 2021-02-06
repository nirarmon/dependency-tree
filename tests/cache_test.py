import pytest
from cache_manager import CacheException, InMemoryCache

@pytest.fixture
def empty_cache():
    '''return a new cache'''
    return InMemoryCache()

@pytest.fixture
def cache_with_packages():
    '''return a new cache'''
    cache = InMemoryCache()
    cache.add_package('access','1.0.1')
    cache.add_package('express','1.0.1','access','1.0.1')
    cache.add_package('express','1.0.1','on-finished','1.0.1')

    return cache

@pytest.fixture
def cache_with_latest_version():
    '''return a new cache'''
    cache = InMemoryCache()
    cache.update_latest_version('express','1.0.1')

    return cache

@pytest.fixture
def cache_with_renderd_tree():
    cache = InMemoryCache()
    cache.add_rendered_tree('express','1.0.0','tree')
    return cache

def test_get_not_exsiting_package_return_empty_array(empty_cache):
    package = empty_cache.get_package('access','1.0.1')
    assert package == []

def test_get_package_witout_dependencie_success(cache_with_packages):
    package = cache_with_packages.get_package('access','1.0.1')
    assert package == []

def test_get_package_with_dependencies_success(cache_with_packages):
    package = cache_with_packages.get_package('express','1.0.1')
    assert len(package)==2
    assert package[0]=='access_1.0.1'
    assert package[1]=='on-finished_1.0.1'

def test_validate_not_existing_package_returns_false(cache_with_packages):
    result = cache_with_packages.validate_package_exists('somePackage','1.0.1')
    assert result is False

def test_validate_existing_package_returns_true(cache_with_packages):
    result = cache_with_packages.validate_package_exists('express','1.0.1')
    assert result is True

def test_get_latest_version_not_exsiting_package(cache_with_packages):
    result = cache_with_packages.get_latest_version('somePackage')
    assert result == 'latest'

def test_get_latest_version_existing_package(cache_with_latest_version):
    result = cache_with_latest_version.get_latest_version('express')
    assert result != 'latest'

def test_update_latest_version_existing_package(cache_with_latest_version):
    result = cache_with_latest_version.get_latest_version('express')
    assert result != 'latest'
    cache_with_latest_version.update_latest_version('express','1.0.3')
    result = cache_with_latest_version.get_latest_version('express')
    assert result == '1.0.3'

def test_update_latest_version_not_existing_package(cache_with_latest_version):
    result = cache_with_latest_version.get_latest_version('somePackage')
    assert result == 'latest'
    cache_with_latest_version.update_latest_version('somePackage','1.0.3')
    result = cache_with_latest_version.get_latest_version('somePackage')
    assert result == '1.0.3'

def test_get_not_existing_tree_from_empty_cache_return_none(empty_cache):
    result =  empty_cache.get_rendered_tree('somePackage','1.0.1')
    assert result is None

def test_get_existing_tree_return_tree(cache_with_renderd_tree):
    result =  cache_with_renderd_tree.get_rendered_tree('express','1.0.0')
    assert result is not None
    assert result == 'tree'

def test_validate_existing_tree_return_true(cache_with_renderd_tree):
    result =  cache_with_renderd_tree.validate_rendered_tree('express','1.0.0')
    assert result is True

def test_validate_not_existing_tree_return_false(cache_with_renderd_tree):
    result =  cache_with_renderd_tree.validate_rendered_tree('somePackage','1.0.0')
    assert result is False
