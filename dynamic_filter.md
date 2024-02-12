# Dynamic Filter Usage 
This serves to provide guidance on the use of the queries to return filtered results.

Filtering works with any of the fields returned by the resource with the following data types:
1. String
2. Boolean
3. Enum
4. Integer
5. Float
6. DateTime

## Filtering
Filtering is implemented using query parameters. 
### Filtering without prefixes
#### URL formatting
```
/api/v1/<resource>?<Param>=<evaluator>
```
where:

  -  `resource` - resource to filter 
  -  `Param` - Field to perform filter on
  - `evaluator` - the check on the param passed
#### 
The `Param` data-types are evaluated to the following operator:

| Data type | Operator | Example                  | Filter description                                          |
| --------- | -------- | :----------------------- | :---------------------------------------------------------- |
| Boolean   | Equal    | True/False               | returns records with the complete likeness of the evaluator |
| DateTime  | Equal    | 2019-02-14(`YYYY-MM-DD`) | returns records with the complete likeness of the evaluator |
| Enum      | Equal    | pending,in_progress      | returns records with the complete likeness of the evaluator |
| Float     | Equal    | 20.0                     | returns records with the complete likeness of the evaluator |
| String    | Like     | this is a string         | returns records with the resemblance of the evaluator       |
#### Examples 
- Filtering with a field with string data-type
    ```
    1. /api/v1/assets?assetCategoryId=-LXSivhFQIkttL7xGSvl
    2. /api/v1/assets?assetCategoryId=-LXSivhFQIkttL7xG
    ```
    ```
    1. /api/v1/requests?subject=Dongle is missing
    2. /api/v1/requests?subject=Dongle
    ```
    _Queries 2 will return records included in Queries 1_

    _Strictly `equal to` filtering is currently not supported_


- Filtering with `enum` field
    - Filtering with valid `enum` evaluator
    ```
        /api/v1/requests?status=completed
    ```
    _This would return request records with a status of completed_

    - Filtering with valid `enum` evaluator
    ```
        /api/v1/requests?status=invalid
    ```
    _This would return an error that the evaluator is invalid_


- Filtering with `DateTime` field

    The `DateTime` evaluator should be in the format `YYYY-MM-DD` else an error is returned
    - Filtering with valid date format
    ```
        /api/v1/requests?dueBy=2019-02-01
    ```
    _This would return request records with a due date `2019-02-01`_

    - Filtering with an invalid valid date format
    ```
        /api/v1/requests?dueBy=2019-02-
    ```
    _This would return an error that the date format is invalid_
#### Note:
- The evaluator for an `enum field ` should be among the items in the enumerator list e.g for the status field of a request, the values should be `completed`, `in_progress`, `open` , `closed`
- Filtering by `description` and `attachments` fields is not implemented.
- Filtering records by a user is only implemented with their `token_id`. 

### Searching using prefixes 
#### `start` prefix (Filtering by greater than)
This is used to filter records `greater than` the value given.
This works with a field that expect following data types

- Dates i.e (`YYYY-MM-DD`)
- Integer i.e (`1,2,3`)
##### URL formatting
```
/api/v1/<resource>?start<Param>=<evaluator>
```
where:

- `resource` - resource to filter 
- `Param` - Field to perform filter on
- `evaluator` - the check on the param passed

##### Examples
- Get all requests created after the date `2019-01-01`
    ```
    /api/v1/requests?startCreatedAt=2019-01-01
    ```
- Get analytics with stock count greater than 50
    ```
    /api/v1/assets/analytics?startStockCount=50
    ```
##### Note:
- Passing a different datatype other than what the field expects would return an error
- Passing an invalid column name will return an error

#### `end` prefix (Filtering by less than or equal to)
This is used to filter records which are `less than or equal to` the value given.
This works with a field that expects following data types

- Dates i.e (`YYYY-MM-DD`)
- Integer i.e (`1,2,3`)

##### URL formatting
```
/api/v1/<resource>?end<Param>=<evaluator>
```
where:

   - `resource` - resource to filter 
  - `Param` - Field to perform filter on
   - `evaluator` - the check on the param passed
##### Examples
- Get all requests created before the date `2019-01-01`
    ```
    /api/v1/requests?endCreatedAt=2019-01-01
    ```
- Get analytics with stock count less than 50
    ```
    /api/v1/assets/analytics?endStockCount=50
    ```
##### Note:
- Passing a different datatype other than what the field expects would return an error
- Passing an invalid column name will return an error


#### `where` prefix (deprecated)
This filters resources using the URL format below:
##### URL format

```
    /api/v1/<resource>?where=<param>,<operator>,<evaluator>
```
where:

-  `resource` - resource to filter 
-  `param` - Field to perform filter on
-  `operator` - type of check to perform 
- `evaluator` - the check on the param passed

##### Possible operators
These operators perform the following evaluations on resources:

| Operator | Operation description                                                           |
| -------- | :------------------------------------------------------------------------------ |
| 'eq'     | returns records with the complete likeness of the evaluator in the param column |
| 'ge'     | returns records greater than or equal the evaluator in the param column         |
| 'gt'     | returns records greater than the evaluator in the param column                  |
| 'le'     | returns records less than or equal the evaluator in the param column            |
| 'like'   | returns records with the resemblance of the evaluator                           |
| 'lt'     | returns records less than the evaluator in the param column                     |
| 'ne'     | returns records no equal the evaluator in the param column                      |

##### Examples
##### Get all request with and open status ( `eq` ) 
```
    /api/v1/requests?where=status,eq,open
```

##### Get all requests with made after a given date ( `ge` ) 
```
    /api/v1/requests?where=created_at,ge,2018-12-18
```
##### Get all requests with made before a given date ( `le` ) 
```
    /api/v1/requests?where=created_at,le,2018-12-18
```
##### Get all requests with made before a given date ( `lt` ) 
```
    /api/v1/requests?where=created_at,lt,2018-12-18
```

##### Get all request which are not open ( `ne` ) 
```
    /api/v1/requests?where=status,ne,open
```
##### Get all records whose subject has Dongle 
```
    /api/v1/requests?where=subject,like,Dongle
```
### Chaining filters
To above filters can be used together using the `&` operator on the URL to achieve filtering with more than one parameter.  

#### Filtering by range 
The `end` and `start` prefix can be used together to get ranges of records
You can also use the `where` prefix (deprecated)
 
##### Examples
- Get all requests created between the date `2019-01-01` and `2019-02-03`
    - using prefixes
    ```
        /api/v1/requests?startCreatedAt=2019-01-01&endCreatedAt=2019-03-01
    ```
    - using where

    ```
        /api/v1/requests?where=created_at,ge,2019-01-01&where=created_at,le,2019-03-01
    ```
- Get analytics with stock count between 50 and 30
    - using prefixes
    ```
        /api/v1/assets/analytics?endStockCount=50&startStockCount=10
    ```
    - using where

    ```
        /api/v1/assets/analytics?where=stock_count,ge,10&where=stock_count,le,50
    ```
#### Filtering by range plus other parameters 
This is done using the `start`, `end` and a `param`

##### Example
- Get all requests created between the date `2019-01-01` and `2019-02-03` with a `serialNumber ` equal to `30`
    ```
    /api/v1/requests?startCreatedAt=2019-01-01&endCreatedAt=2019-03-01&serialNumber=30
    ```
#### Filtering by assignee and status
```
    /api/v1/requests?assigneeId=2019-01-01&status=
```