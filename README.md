# dependency-tree
<img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/nirarmon/dependency-tree/Python%20application?style=plastic">

this project is a web application that gets an npm package name and version and returens the packages's dependecies tree
### Code Structure
the code have 3 main classes (other than the api controller), all classes implements their respective interface 
##### NPMRegistryClient (implements IRegiteryClient)
retrive data from [npmjs](https://registry.npmjs.org/ "npmjs")
##### InMemoryCache (implements ICacheManager)
saves the dependcies tree data in dictioneries where the key is the root package and the value is a list of dependencies
##### NPMDependenciesTree (implements IDependencyTree)
holds the NPM tree logic - build and saves the dependencies tree of a requested package
##### HtmlTreeRenderer (implements IdependencyTreeRenderer)
build an HTML tree of a specific package
### API Strcture
GET and POST can handle both sepcific version and latest version
#### POST
The POST method only save the package tree in the application memory
exmple of post body:
```bash
curl --location --request POST 'http://<server_url>/packages' \
--header 'Content-Type: application/json' \
--data-raw '{"package":"access","version":"latest"}'
```

possible status codes:

|  Status Code | Reason  |
| :------------ | :------------ |
| 400  | bad request, some of the request paramters are missing in the request body  |
| 404  | package not found / package deprecated  |
| 503  | inernal server error |
| 200 | package was succsessfuly added, a sucess json will be returned |

#### GET
The GET method will save the package tree and returns an HTML that represents the depndncies tree

GET example:
```bash
    curl --location --request GET 'http://<server_url>/packages?package=access&version=1.0.1'
```
possible status codes:

|  Status Code | Reason  |
| :------------ | :------------ |
| 400  | bad request, some of the request paramters are missing in the request query  |
| 404  | package not found / package deprecated  |
| 503  | inernal server error |
| 200| the service will retuen an HTML with the dependency tree|
sucess json
```json
{"success": true, "message": "package was added"}
```
#### PUT
The PUT method updatd all packages latest version if needed
PUT example:
```bash
curl --location --request PUT 'http://127.0.0.1:5000/packages'
```
possible status codes:

|  Status Code | Reason  |
| :------------ | :------------ |
| 404  | package not found / package deprecated  |
| 503  | inernal server error |
| 200 | package was succsessfuly added, a sucess json will be returned  |

sucess json
```json
{"success": true, "message": "all latest versions were updated"}
```
