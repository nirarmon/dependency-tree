import abc
import requests
import json 

class IRegiteryClient(abc.ABC):
    @abc.abstractmethod
    def getPackageInfromation(self,package,version):
        pass

class NPMRegistryClient(IRegiteryClient):

    def __init__(self,baseUrl):
        self.__baseUrl = baseUrl
        pass

    def getPackageInfromation(self,package,version):     
        r =requests.get(self.__baseUrl+package+'/'+version)
        if r.status_code == requests.codes.ok:
            return json.loads(r.text)
        if r.status_code > 400 and r.status_code < 500:
            raise PackageNotFoundExcetion(package,version)
        if r.status_code > 500 and r.status_code < 600:
            raise ServerErrorExcetion(baseUrl)

class PackageNotFoundExcetion(Exception):
    def __init__(self, package,version):
        self.message = 'Could not find package: '+package+':'+version
        super().__init__(self.message)

class ServerErrorExcetion(Exception):
    def __init__(self, baseUrl):
        self.message ="Server Error - Cannot Access "+baseUrl
        super().__init__(self.message)