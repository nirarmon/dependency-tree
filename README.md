# dependency-tree
<img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/nirarmon/dependency-tree/Python%20application?style=plastic">

### Assumptions (a.k.a What I should've done better)
1. **In memory cache** -I used in memory data structure, in real life scenario I would've use a mix of a database and distributed cache like Redis, though Redis can play both parts in this scenario
2. **Lazy Init vs Warmup** - I used lazy init meaning the data is being saved on the fly when trying to get a new package, later on the data will be retrieved from cache if the data already exists, this is for the original package and the it's sub packages
I also saved the HTML tree for better performance. 
In real life scenario I would've consider cache/data warmup saving all packages (or the most searched) in cache when the server starts, the down side of this method is the deployment cost (which can be optimized) but I think it worth it in performance
3. **package update** - I assumed that only the latest version can be updated, meaning, a new version is now the latest all other versions cannot be changed. 
for example: express 4.17.2 is now the latest version of express and not 4.17.1
to update the latest version, I saved all latest versions in memory and added a PUT API call that can be executed by a scheduler and updates all latest version and their dependencies tree.
In real life, I would've use API hooks [as described here  ](http://https://github.com/npm/registry/blob/master/docs/hooks/creating-and-managing-hooks.md "as described here  ") 
4. **circular dependencies** - are the devil and therefore are not supported
5. **semantic versioning** - the code does not support "acceptable version ranges" only simple semantic versioning i.e. ~1.13.1 will count as 1.13.1
6. **more tests**

### Code Structure
3 main classes (other than the api controller), all classes implements their respective interface 
##### NPMRegistryClient (implements IRegiteryClient)
retrieves data from [npmjs](https://registry.npmjs.org/ "npmjs")
##### InMemoryCache (implements ICacheManager)
saves the dependencies tree data in dictionaries where the key is the root package and the value is a list of dependencies
##### NPMDependenciesTree (implements IDependencyTree)
holds the NPM tree logic - build and saves the dependencies tree of a requested package
##### HtmlTreeRenderer (implements IdependencyTreeRenderer)
build an HTML tree of a specific package
### API Structure
GET and POST can handle both specific version and latest version
#### POST
The POST method only save the package tree in the application memory
example of post body:
```bash
curl --location --request POST 'http://<server_url>/packages' \
--header 'Content-Type: application/json' \
--data-raw '{"package":"access","version":"latest"}'
```

possible status codes:

|  Status Code | Reason  |
| :------------ | :------------ |
| 400  | bad request, some of the request parameters are missing in the request body  |
| 404  | package not found / package deprecated  |
| 503  | internal server error |
| 200 | package was successfully added, a success json will be returned |

#### GET
The GET method will save the package tree and returns an HTML that represents the dependencies tree
the GET call relays on calling the POST call first, but for this assignment as I used lazy loading of the data it also saves the data before getting it from memory
**please note:** at first, the GET method will take some time to return response as the data structure is being built on the fly, later GET calls might return from cache

GET example:
```bash
    curl --location --request GET 'http://<server_url>/packages?package=access&version=1.0.1'
```
possible status codes:

|  Status Code | Reason  |
| :------------ | :------------ |
| 400  | bad request, some of the request parameters are missing in the request query  |
| 404  | package not found / package deprecated  |
| 503  | internal server error |
| 200| the service will returns an HTML with the dependency tree|
success json
```json
{"success": true, "message": "package was added"}
```
#### PUT
The PUT method updated all packages latest version if needed and saves their respective dependencies trees, therefore this call might be heavy and slow
PUT example:
```bash
curl --location --request PUT 'http://127.0.0.1:5000/packages'
```
possible status codes:

|  Status Code | Reason  |
| :------------ | :------------ |
| 404  | package not found / package deprecated  |
| 503  | internal server error |
| 200 | package was successfully added, a success json will be returned  |

success json
```json
{"success": true, "message": "all latest versions were updated"}
```

