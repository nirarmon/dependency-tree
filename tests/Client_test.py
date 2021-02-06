from registry_client import NPMRegistryClient, PackageNotFoundExcetion, ServerErrorExcetion
import pytest
from requests.exceptions import Timeout
import requests

class MockResponse(object):
    def __init__(self,status_code,text=None):
        self.status_code = status_code
        self.text = text

@pytest.fixture
def mock_response_200(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse(200,'{\"name\":\"access\",\"version\":\"1.0.2\",\"description\":\"Get deeply nested values from unknown shapes with at-runtime type safety.\",\"main\":\"./lib/index.js\",\"types\":\"./lib/index.d.ts\",\"author\":{\"name\":\"Conor Davidson\",\"email\":\"conor@conordavidson.com\"},\"license\":\"MIT\",\"scripts\":{\"build\":\"tsc --pretty\",\"test\":\"jest --coverage\",\"test:cover\":\"jest && codecov\"},\"jest\":{\"testRegex\":\".*/*.test.ts$\",\"moduleFileExtensions\":[\"js\",\"ts\"],\"transform\":{\"\\\\.ts$\":\"ts-jest\"},\"coverageDirectory\":\"./coverage/\",\"collectCoverage\":true},\"devDependencies\":{\"@types/jest\":\"^24.0.15\",\"codecov\":\"^3.5.0\",\"jest\":\"^24.8.0\",\"ts-jest\":\"^24.0.2\",\"typescript\":\"^3.5.2\"},\"gitHead\":\"6a86444cb84e6cc09528355c9da9e3e40fb29e52\",\"_id\":\"access@1.0.2\",\"_npmVersion\":\"5.6.0\",\"_nodeVersion\":\"8.11.1\",\"_npmUser\":{\"name\":\"conordavidson\",\"email\":\"conor@conordavidson.com\"},\"dist\":{\"integrity\":\"sha512-f8nS8zB/1DEXSqJlM+oBYj/DeW6cJB/+7rQNoKHZylaBROCoomApKtUHITCXp7crJvHhviQJQ+cYJ7RdRoIXjA==\",\"shasum\":\"93a8d2e9452e8a78bfd85b6846d98727592089cd\",\"tarball\":\"https://registry.npmjs.org/access/-/access-1.0.2.tgz\",\"fileCount\":23,\"unpackedSize\":56678,\"npm-signature\":\"-----BEGIN PGP SIGNATURE-----\\r\\nVersion: OpenPGP.js v3.0.4\\r\\nComment: https://openpgpjs.org\\r\\n\\r\\nwsFcBAEBCAAQBQJdQhrpCRA9TVsSAnZWagAAqr8P/21UHEfZU7FPOvv/pq5z\\nBY6hMnIBCw2qUlwK9oBdUoiAVNfzwAZJMmDi+tHmf3dgAy5NJgBIVc6NrIiF\\n/ruruvfrYOjt3FOBX+1Gu8+FKyotyrBZZ346i2juD+ppPKdKdg/R4ZPJ98K/\\nNTwwzkJVhPEd992Eojo1jDeDEvNBPuGAaW5tbPyb7tFp+ZzfYwQJKK4xhrrN\\nuhIJwphSO4Imo5/pEBZxjiaRQDB6MYimYKK8xze5sE0t2aVROLlPRIvxJ7e0\\nD6xlMEfkNMwajctOpSYQF1bPWcGpA2vpELpMGzx4kDTzkOtrc47QffpzdBW9\\na/xAKR2+0/PGYZ3xKjiHd9SJlkx7ux7YUJO9oAC0m5WoZ33l5aEd8dLKxThl\\nJ4OCw/dQ29GqiT3Nx3s4eG5D0/rNiYFVMz25GwPJblBwyNgi84z5sLsUkNXC\\nNChP7CWI6m/n065xsYfvmm7d91JJezoyIvpUHeX+5aG5xnCXLFtQJPsjb2kG\\nUAAi+ugRSuqIJVEvko+W86GM75trmjwc3AAxUa9xs2R3HAaaMiTI/NigW3+x\\nq6k69b/uJZJ1ArLouAnm62fANIPYRlpJ8nQbtjyXEUPlH4O3loQ8TwHsfRqH\\ndEK55QVO/yaa2aIgFVfGgNVBZsFDWTa2EaPxhZx/MLzXj2aQvu3nZ0FbqW14\\nJKnP\\r\\n=5uAZ\\r\\n-----END PGP SIGNATURE-----\\r\\n\"},\"maintainers\":[{\"email\":\"conor@conordavidson.com\",\"name\":\"conordavidson\"}],\"directories\":{},\"_npmOperationalInternal\":{\"host\":\"s3://npm-registry-packages\",\"tmp\":\"tmp/access_1.0.2_1564613351816_0.33768296794615327\"},\"_hasShrinkwrap\":false}')
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
    return NPMRegistryClient('http://registry.npmjs.org/')

def test_get_information_package_not_exists_fail(client,mock_response_404):
    with pytest.raises(PackageNotFoundExcetion):
        client.get_package_infromation('packageNotExists','1.1.1')

def test_get_information_sucsess(client,mock_response_200):
    response = client.get_package_infromation('access','latest')
    assert response['name'] == 'access'
    assert response is not None

def test_get_information_serverError(client,mock_response_503):
    with pytest.raises(ServerErrorExcetion):
        client.get_package_infromation('packageNotExists','1.1.1')