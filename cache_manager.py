import abc
import json 

class ICacheManager(abc.ABC):
    @abc.abstractmethod
    def add_package(self,package,version,dependencies):
        pass
    @abc.abstractmethod
    def validate_package_exists(self,package,version):
        pass
    @abc.abstractmethod
    def get_package(self,package,version):
        pass
    @abc.abstractmethod
    def update_latest_version(self,package,version):
        pass 
    @abc.abstractmethod
    def get_latest_version(self,package,version):
        pass
    @abc.abstractmethod
    def get_rendered_tree(self,package,version):
        pass
    @abc.abstractmethod
    def add_rendered_tree(self,package,version,tree):
        pass
    @abc.abstractmethod
    def validate_rendered_tree(self,package):
        pass
    @abc.abstractmethod
    def get_all_latest_versions(self):
        pass
    @abc.abstractmethod
    def clear_cache(self):
        pass

class InMemoryCache(ICacheManager):

    def __init__(self):
        self.__dependencies_cache = {}
        self.__latest_version_cache = {}
        self.__rendered_trees = {}

    def add_package(self,package,version,dependency=None,dependencyVersion=None):
        """addes a package and its dependencies to the cache"""
        try:
            packageVersion = self.__to_cache_key(package,version)
            if packageVersion not in self.__dependencies_cache.keys():
                self.__dependencies_cache[packageVersion] = []
            if dependency is not None:
                self.__dependencies_cache[packageVersion].append(self.__to_cache_key(dependency,dependencyVersion))
        except Exception as error:
            print(error)
            raise CacheException('Could not add to cache '+package+':'+version)

    def validate_package_exists(self,package,version):
        """validates if a package is in cache cache"""
        try:
            return self.__to_cache_key(package,version) in self.__dependencies_cache.keys()
        except Exception as error:
            print(error)
            raise CacheException('Could not validate cache '+package+':'+version)

    def get_package(self,package,version):
        """gets package dependencies from cahce, will return and empty array if the package does not have any dependencies or not exists"""
        try:
            packageVersion = self.__to_cache_key(package,version)
            if self.__dependencies_cache.get(packageVersion) is None or not self.__dependencies_cache[packageVersion]:
                return []
            return self.__dependencies_cache[packageVersion]
        except Exception as error:
            print(error)
            raise CacheException('Could not get package from cache '+package+':'+version)

    def update_latest_version(self,package,version):
        """updates the latest version of a package"""
        try:
            self.__latest_version_cache[package] = version
        except Exception as error:
            print(error)
            raise CacheException('Could update latest version of '+package+':'+version)

    def get_latest_version(self,package):
        """returns the latest version of a package"""
        try:
            if self.__latest_version_cache.get(package) is None:
                return 'latest'
            return self.__latest_version_cache[package]
        except Exception as error:
            print(error)
            raise CacheException('Could not get latest version of '+package)
    
    def get_all_latest_versions(self):
        """gets all saved packages"""
        return self.__latest_version_cache.keys()   
    
    def get_rendered_tree(self,package,version):
        """get a rendered dependencies tree from cache"""
        try:
            return self.__rendered_trees.get(self.__to_cache_key(package,version))
        except Exception as error:
            print(error)
            raise CacheException('Could update rendered tree cache of '+package+':'+version)

    def add_rendered_tree(self,package,version,tree):
        """add rendered dependencies tree to cahce"""
        try:
            self.__rendered_trees[self.__to_cache_key(package,version)] = tree
        except Exception as error:
            print(error)
            raise CacheException('Could update rendered tree cache of '+package+':'+version)

    def validate_rendered_tree(self,package,version):
        """validate if a rendered tree is already in cahce, return true if it does"""
        try:
            return self.__to_cache_key(package,version) in self.__rendered_trees.keys()
        except Exception as error:
            print(error)
            raise CacheException('Could not validate tree cache of '+package+':'+version)

        def clear_cache(self):
            try:
                self.__dependencies_cache.clear()
            except Exception as error:
                print(error)
                raise CacheException('Could not clear dependencies cache')


    def __to_cache_key(self,package,version):
        return package+'_'+version

class CacheException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


  
