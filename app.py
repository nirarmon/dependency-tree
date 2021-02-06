from markupsafe import escape
from flask import Flask
from dependency_tree import NPMDependenciesTree
from dependency_tree import DependencyException

from cache_manager import InMemoryCache
from cache_manager import CacheException
from registry_client import NPMRegistryClient
from registry_client import PackageNotFoundExcetion
from registry_client import ServerErrorExcetion
from dependency_tree_renderer import HtmlTreeRenderer
from dependency_tree_renderer import RendererException

app = Flask(__name__)

@app.route('/<package>/<version>')
def printPackageTree(package,version):
   
    try:
        tree.build_dependencies_tree(escape(package),escape(version))
        return tree.get_dependencies_tree(escape(package),escape(version))
    except DependencyException as error:
        return error.message,404
    except Exception as error:
        return error.message,503

if __name__ == '__main__':
    tree = NPMDependenciesTree(NPMRegistryClient('http://registry.npmjs.org/'),InMemoryCache(),HtmlTreeRenderer())
    app.run()