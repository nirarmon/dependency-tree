from markupsafe import escape
from flask import Flask
from DependencyTree import NPMDependenciesTree
from DependencyTree import DependencyException

from CacheManager import InMemoryCache
from CacheManager import CacheException
from RegistryClient import NPMRegistryClient
from RegistryClient import PackageNotFoundExcetion
from RegistryClient import ServerErrorExcetion
from DependencyTreeRenderer import HtmlTreeRenderer
from DependencyTreeRenderer import RendererException

app = Flask(__name__)

@app.route('/<package>/<version>')
def printPackageTree(package,version):
   
    try:
        tree.buildDependencyTree(escape(package),escape(version))
        return tree.getDependenciesTree(escape(package),escape(version))
    except DependencyException as error:
        return error.message,404
    except Exception as error:
        return error.message,503

if __name__ == '__main__':
    n = NPMRegistryClient()
    c = InMemoryCache()
    r = HtmlTreeRenderer()
    tree = NPMDependenciesTree(n,c,r)
    app.run()