from RegistryClient import NPMRegistryClient, PackageNotFoundExcetion, ServerErrorExcetion
import pytest


@pytest.fixture
def client():
    '''return a new client'''
    return NPMRegistryClient('http://registry.npmjs.org/')

def test_get_information_package_not_exists_fail(client):
    with pytest.raises(PackageNotFoundExcetion):
        client.getPackageInfromation('packageNotExists','1.1.1')

def test_get_information_sucsess(client):
    response = client.getPackageInfromation('access','latest')
    assert response['name'] == 'access'
    assert response is not None
