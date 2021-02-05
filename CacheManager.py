import abc
import json 

class ICacheManager(abc.ABC):
    @abc.abstractmethod
    def addPackage(self,package,version,dependencies):
        pass
    @abc.abstractmethod
    def validatePackageExists(self,package,version):
        pass
    @abc.abstractmethod
    def getPackage(self,package,version):
        pass
    @abc.abstractmethod
    def updateLatestVersion(self,package,version):
        pass 
    @abc.abstractmethod
    def getLatestVersion(self,package,version):
        pass
    @abc.abstractmethod
    def getRenderedTree(self,package,version):
        pass
    @abc.abstractmethod
    def addRenderedTree(self,package,version,tree):
        pass
    @abc.abstractmethod
    def validateRenderedTree(self,package):
        pass


class InMemoryCache(ICacheManager):

    def __init__(self):
        self.__dependenciesCache = {}
        self.__latestVersionCache = {}
        self.__renderedTrees = {}

    def addPackage(self,package,version,dependency=None,dependencyVersion=None):
        try:
            packageVersion = self.__toCacheKey(package,version)
            if packageVersion not in self.__dependenciesCache.keys():
                self.__dependenciesCache[packageVersion] = []
            if dependency is not None:
                self.__dependenciesCache[packageVersion].append(self.__toCacheKey(dependency,dependencyVersion))
        except Exception as error:
            print(error)
            raise CacheException('Could not add to cache '+package+':'+version)

    def validatePackageExists(self,package,version):
        try:
            return self.__toCacheKey(package,version) in self.__dependenciesCache.keys()
        except Exception as error:
            print(error)
            raise CacheException('Could not validate cache '+package+':'+version)

    def getPackage(self,package,version):
        try:
            packageVersion = self.__toCacheKey(package,version)
            if self.__dependenciesCache.get(packageVersion) is None or not self.__dependenciesCache[packageVersion]:
                return []
            return self.__dependenciesCache[packageVersion]
        except Exception as error:
            print(error)
            raise CacheException('Could not get package from cache '+package+':'+version)

    def updateLatestVersion(self,package,version):
        try:
            self.__latestVersionCache[package] = version
        except Exception as error:
            print(error)
            raise CacheException('Could update latest version of '+package+':'+version)

    def getLatestVersion(self,package):
        try:
            if self.__latestVersionCache.get(package) is None:
                return 'latest'
            return self.__latestVersionCache[package]
        except Exception as error:
            print(error)
            raise CacheException('Could not get latest version of '+package)
        
    
    def getRenderedTree(self,package,version):
        try:
            return self.__renderedTrees.get(self.__toCacheKey(package,version))
        except Exception as error:
            print(error)
            raise CacheException('Could update rendered tree cache of '+package+':'+version)

    def addRenderedTree(self,package,version,tree):
        try:
            self.__renderedTrees[self.__toCacheKey(package,version)] = tree
        except Exception as error:
            print(error)
            raise CacheException('Could update rendered tree cache of '+package+':'+version)

    def validateRenderedTree(self,package,version):
        try:
            return self.__toCacheKey(package,version) in self.__renderedTrees.keys()
        except Exception as error:
            print(error)
            raise CacheException('Could not validate tree cache of '+package+':'+version)


    def __toCacheKey(self,package,version):
        return package+'_'+version

class CacheException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


  
