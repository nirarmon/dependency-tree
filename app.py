from markupsafe import escape
import html
from flask import Flask
from flask import request
from dependency_tree import NPMDependenciesTree
from dependency_tree import DependencyException
import json

from cache_manager import InMemoryCache
from cache_manager import CacheException
from registry_client import NPMRegistryClient
from registry_client import PackageNotFoundExcetion
from registry_client import ServerErrorExcetion
from dependency_tree_renderer import HtmlTreeRenderer
from dependency_tree_renderer import RendererException

app = Flask(__name__)

@app.route('/packages',methods=['GET'])
def printPackageTree():
    if request.args:
        args = request.args
    package = request.args.get('package')
    version = request.args.get('version')
    if package is None:
        return 'call must contain package name',400
    if version is None:
        return 'call must contain package version',400
    try:
        tree.build_dependencies_tree(escape(package),escape(version))
        html_body = html.unescape(tree.get_dependencies_tree(escape(package),escape(version)))
        return html.unescape(html_body)
    except DependencyException as error:
        return error.message,404
    except Exception as error:
        return 503

@app.route('/packages',methods=['POST'])
def save_package():
    if not request.json:
        return 'request must contain json body',400
    if 'package' not in request.json :
        return 'body must contain package name',400
    if 'version' not in request.json:
        return 'body must contain package version',400
    try:
        tree.build_dependencies_tree(request.json['package'],request.json['version'])
        return json.dumps({'success':True,'message':'package was added'}), 200, {'ContentType':'application/json'} 
    except DependencyException as error:
        return error.message,404
    except Exception as error:
        return 'internal server error', 503

@app.route('/packages',methods=['PUT'])
def update():
    try:
        tree.update_latest_versions()
        return json.dumps({'success':True,'message':'all latest versions were updated'}), 200, {'ContentType':'application/json'} 
    except DependencyException as error:
        return error.message,404
    except Exception as error:
        return error.message,503

@app.route('/packages',methods=['DELETE'])
def clear():
    try:
        tree.clear_dependencies_data()
        return json.dumps({'success':True,'message':'cahce was cleared'}), 200, {'ContentType':'application/json'} 
    except DependencyException as error:
        return error.message,404
    except Exception as error:
        return error.message,503

@app.route('/',methods=['GET'])
def default():
    try:
        search_page = (
            "<!DOCTYPE html>"
            "<html>"
            "<head>"
            "<meta charset='UTF-8'>"
            "<title>Dependency Tree Search</title>"
            "</head>"
            "<body>"
            "<form action='/packages' method='get' style='margin-bottom:20px;'>"
            "<input type='text' name='package' placeholder='Package name' required>"
            "<input type='text' name='version' value='latest'>"
            "<button type='submit'>Search</button>"
            "</form>"
            "</body>"
            "</html>"
        )
        return html.unescape(search_page)
    except DependencyException as error:
        return error.message,404
    except Exception as error:
        return 503

if __name__ == '__main__':
    tree = NPMDependenciesTree(NPMRegistryClient('http://registry.npmjs.org/'),InMemoryCache(),HtmlTreeRenderer())
    app.run()