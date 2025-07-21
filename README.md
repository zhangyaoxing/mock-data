# mock-data
Generate mock data for MongoDB follow configured rules.

## Dependencies
- Python 3.11.12
- Libraries:
```bash
pip install -r requirements.txt
```

## Date Type Definition
The following data types are supported by this tool. Use `Number` or `Alias` when you define the data type for mock data.
|        Type        | Number |   Alias    | Supported |
|:------------------:|:------:|:----------:|:---------:|
|       Double       |   1    |   double   |  &check;  |
|       String       |   2    |   string   |  &check;  |
|       Object       |   3    |   object   |  &check;  |
|       Array        |   4    |   array    |  &check;  |
|    Binary data     |   5    |  binData   |  &check;  |
|      ObjectId      |   7    |  objectId  |  &check;  |
|      Boolean       |   8    |    bool    |  &check;  |
|        Date        |   9    |    date    |  &check;  |
|        Null        |   10   |    null    |  &check;  |
| Regular Expression |   11   |   regex    |  &check;  |
|     JavaScript     |   13   | javascript |  &check;  |
|   32-bit integer   |   16   |    int     |  &check;  |
|     Timestamp      |   17   | timestamp  |  &check;  |
|   64-bit integer   |   18   |    long    |  &check;  |
|     Decimal128     |   19   |  decimal   |  &check;  |
|      Min key       |   -1   |   minKey   |  &cross;  |
|      Max key       |  127   |   maxKey   |  &check;  |

## How to Use
The tool utilizes JSON schema, which is also used by MongoDB schema validator, to define data schema. Because Json schema doesn't have the definition for values, we utlize the value description in the `description` field.  
Allowed values include:  
// TODO: possible values from Faker library.