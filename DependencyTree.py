import abc
import re
from queue import LifoQueue, Queue
from DependencyTreeRenderer import RendererException
from CacheManager import CacheException
from RegistryClient import PackageNotFoundExcetion, ServerErrorExcetion


class IDependencyTree(abc.ABC):
    @abc.abstractmethod
    def buildDependencyTree(self,package,version):
        pass
    
    @abc.abstractmethod
    def getDependenciesTree(self,package,version):
        pass


class NPMDependenciesTree(IDependencyTree):

    def __init__(self,npmRegisteryClient,cache,treeRenderer):
        self.__client = npmRegisteryClient
        self.__cache = cache
        self.__treeRenderer = treeRenderer

    def buildDependencyTree(self,package,version):
        try:
            #if version is latest get the latest version
            if version=='latest':
                version = self.__cache.getLatestVersion(package)
            #validate if already in cache
            if self.__cache.validatePackageExists(package,version):
                return '' #already in cache
            queue = Queue()
            visted = []
            rootPackage = self.__client.getPackageInfromation(package,version)
            rootPackageVersion = rootPackage['version']
            #this is the first time that latest version is udpated
            if version == 'latest':
                self.__cache.updateLatestVersion(package,rootPackageVersion)
            #if the package has no dependencies
            if ('dependencies') not in rootPackage.keys():
                self.__cache.addPackage(package,rootPackageVersion)
                return True
            #if the package has dependencies 
            dependencies = rootPackage['dependencies']
            for dependency in dependencies:
                dependencyVersion = self.__getVersion(dependencies[dependency])
                queue.put((dependency,dependencyVersion))
                self.__cache.addPackage(package,rootPackageVersion,dependency,dependencyVersion)     
            #itrate over all dependencies and sub dependencies
            while queue.empty()==False:
                (currentDependencyPackageName,currentPackageVersion) = queue.get()
                # if dependecy is already cached
                if self.__cache.validatePackageExists(currentDependencyPackageName,currentPackageVersion):
                    continue
                # get dependency information
                dependencyInformation = self.__client.getPackageInfromation(currentDependencyPackageName,currentPackageVersion)
                # if dependecy has no sub dependecies
                if ('dependencies') not in dependencyInformation.keys():
                    self.__cache.addPackage(currentDependencyPackageName,currentPackageVersion)
                    continue
                #if the dependecy has sub dependencies
                dependencies = dependencyInformation['dependencies']
                for dependency in dependencies:
                    dependencyVersion = self.__getVersion(dependencies[dependency])
                    queue.put((dependency,dependencyVersion))
                    self.__cache.addPackage(currentDependencyPackageName,currentPackageVersion,dependency,dependencyVersion)  
            return True
        except PackageNotFoundExcetion as error:
            print(error)
        except ServerErrorExcetion as error:
            print(error)
            raise Exception('Server Error '+error.message)
        except CacheException as error:
            print(error)
            raise Exception('Cache Error '+ error.message)

    def getDependenciesTree(self,package,version):
        try:
            self.__treeRenderer.clear()
            # get latest version
            if version=='latest':
                version = self.__cache.getLatestVersion(package)
            # validate that the package is already cahced
            if not self.__cache.validatePackageExists(package,version):
                raise DependencyException('Cound not find package '+package+':'+'version')
            # validate if package is already rendedred 
            if self.__cache.validateRenderedTree(package,version):
                return self.__cache.getRenderedTree(package,version)
            stack = LifoQueue()
            stack.put((package,version))
            while stack.empty() == False:
                (currPackageName,currPackageVersion) = stack.get()
                dependencies = self.__cache.getPackage(currPackageName,currPackageVersion)
                if not dependencies:
                    self.__treeRenderer.addNewEntry(currPackageName+':'+currPackageVersion)
                    self.__treeRenderer.endLevel()
                else:
                    self.__treeRenderer.addNewEntry(currPackageName+':'+currPackageVersion)
                    for value in dependencies:
                        (currPackageName,currPackageVersion) = value.split('_')
                        stack.put((currPackageName,currPackageVersion))
                    self.__treeRenderer.startNewLevel()
            # render the tree and save it in cache 
            renderedTree = self.__treeRenderer.render()
            self.__cache.addRenderedTree(package,version,renderedTree)
            return renderedTree
        except RendererException as error:
            print(error)
            raise Exception('error rendering tree '+error.message)
        except CacheException as error:
            print(error)
            raise Exception('error while trying to access cache '+error.message)


    def __getVersion(self,version):
        matchObj = re.match( r'\D*(\d*\.\d*\.\d*)', version)
        return matchObj.group(1)

class DependencyException(Exception):
    def __init__(self, message):
        self.message =message
        super().__init__(self.message)

