import abc
import re
from queue import LifoQueue, Queue
from dependency_tree_renderer import RendererException
from cache_manager import CacheException
from registry_client import PackageNotFoundExcetion, ServerErrorExcetion


class IDependencyTree(abc.ABC):
    @abc.abstractmethod
    def build_dependencies_tree(self,package,version):
        pass
    
    @abc.abstractmethod
    def get_dependencies_tree(self,package,version):
        pass


class NPMDependenciesTree(IDependencyTree):

    def __init__(self,npm_registery_client,cache,tree_renderer):
        self.__client = npm_registery_client
        self.__cache = cache
        self.__tree_renderer = tree_renderer

    def build_dependencies_tree(self,package,version):
        try:
            #if version is latest get the latest version
            if version=='latest':
                version = self.__cache.get_latest_version(package)
            #validate if already in cache
            if self.__cache.validate_package_exists(package,version):
                return '' #already in cache
            queue = Queue()
            visted = []
            root_package = self.__client.get_package_infromation(package,version)
            root_package_version = root_package['version']
            #this is the first time that latest version is udpated
            if version == 'latest':
                self.__cache.update_latest_version(package,root_package_version)
            #if the package has no dependencies
            if ('dependencies') not in root_package.keys():
                self.__cache.add_package(package,root_package_version)
                return True
            #if the package has dependencies 
            dependencies = root_package['dependencies']
            for dependency in dependencies:
                dependency_version = self.__get_version(dependencies[dependency])
                queue.put((dependency,dependency_version))
                self.__cache.add_package(package,root_package_version,dependency,dependency_version)     
            #itrate over all dependencies and sub dependencies
            while queue.empty()==False:
                (current_dependency_package_name,current_package_version) = queue.get()
                # if dependecy is already cached
                if self.__cache.validate_package_exists(current_dependency_package_name,current_package_version):
                    continue
                # get dependency information
                dependency_information = self.__client.get_package_infromation(current_dependency_package_name,current_package_version)
                # if dependecy has no sub dependecies
                if ('dependencies') not in dependency_information.keys():
                    self.__cache.add_package(current_dependency_package_name,current_package_version)
                    continue
                #if the dependecy has sub dependencies
                dependencies = dependency_information['dependencies']
                for dependency in dependencies:
                    dependency_version = self.__get_version(dependencies[dependency])
                    queue.put((dependency,dependency_version))
                    self.__cache.add_package(current_dependency_package_name,current_package_version,dependency,dependency_version)  
            return True
        except PackageNotFoundExcetion as error:
            print(error)
        except ServerErrorExcetion as error:
            print(error)
            raise Exception('Server Error '+error.message)
        except CacheException as error:
            print(error)
            raise Exception('Cache Error '+ error.message)

    def get_dependencies_tree(self,package,version):
        try:
            self.__tree_renderer.clear()
            # get latest version
            if version=='latest':
                version = self.__cache.get_latest_version(package)
            # validate that the package is already cahced
            if not self.__cache.validate_package_exists(package,version):
                raise DependencyException('Cound not find package '+package+':'+'version')
            # validate if package is already rendedred 
            if self.__cache.validate_rendered_tree(package,version):
                return self.__cache.get_rendered_tree(package,version)
            stack = LifoQueue()
            stack.put((package,version))
            while stack.empty() == False:
                (current_package_name,current_package_version) = stack.get()
                dependencies = self.__cache.get_package(current_package_name,current_package_version)
                if not dependencies:
                    self.__tree_renderer.add_new_entry(current_package_name+':'+current_package_version)
                    self.__tree_renderer.end_level()
                else:
                    self.__tree_renderer.add_new_entry(current_package_name+':'+current_package_version)
                    for value in dependencies:
                        (current_package_name,current_package_version) = value.split('_')
                        stack.put((current_package_name,current_package_version))
                    self.__tree_renderer.start_new_level()
            # render the tree and save it in cache 
            renderedTree = self.__tree_renderer.render()
            self.__cache.add_rendered_tree(package,version,renderedTree)
            return renderedTree
        except RendererException as error:
            print(error)
            raise Exception('error rendering tree '+error.message)
        except CacheException as error:
            print(error)
            raise Exception('error while trying to access cache '+error.message)


    def __get_version(self,version):
        matchObj = re.match( r'\D*(\d*\.\d*\.\d*)', version)
        return matchObj.group(1)

class DependencyException(Exception):
    def __init__(self, message):
        self.message =message
        super().__init__(self.message)

