# MockData - Flexible Mock Data Generator

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A flexible and powerful mock data generator based on JSON schemas. Built on top of [Faker](https://faker.readthedocs.io/), MockData generates realistic test data for MongoDB, Kafka, and file-based outputs in [EJSON](https://www.mongodb.com/docs/manual/reference/mongodb-extended-json/) format.

## Features

- 📝 **Schema-driven**: Define data structures using JSON Schema
- 🎲 **Faker integration**: Leverage all Faker providers for realistic data
- 🔌 **Multiple outputs**: Support for EJSON files, MongoDB, and Kafka
- 🏗️ **Extensible**: Easy to add custom providers and data types
- 🚀 **Production-ready**: Proper package structure with tests and documentation
- ⚡ **Batch processing**: Efficient bulk operations for database outputs

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/mockdata.git
cd mockdata

# Install in development mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

### Using pip (when published)

```bash
pip install mockdata
```

## Quick Start

1. **Define your schema** in the `schemas/` directory (e.g., `schemas/users.json`):

```json
{
  "name": "users",
  "count": 100,
  "$jsonSchema": {
    "properties": {
      "name": {
        "bsonType": "string",
        "description": "#name()#"
      },
      "email": {
        "bsonType": "string",
        "description": "#email()#"
      },
      "age": {
        "bsonType": "int",
        "description": "#random_int(18, 80)#"
      }
    }
  }
}
```

2. **Configure outputs** in `config/config.json` or `config.json`:

```json
{
  "output": {
    "ejson": {
      "folder": "data"
    }
  }
}
```

3. **Run the generator**:

```bash
# Using the installed command
mockdata

# Or as a module
python -m mockdata
```

## Project Structure

```
mockdata/
├── src/
│   └── mockdata/
│       ├── __init__.py
│       ├── __main__.py          # CLI entry point
│       ├── core/                # Core functionality
│       │   ├── mock_data.py     # Main generator class
│       │   ├── constants.py     # BSON type definitions
│       │   └── fake_providers.py # Custom Faker providers
│       ├── providers/           # Output providers
│       │   ├── base.py
│       │   ├── ejson.py
│       │   ├── mongodb.py
│       │   └── kafka.py
│       └── utils/               # Utility modules
│           ├── config.py
│           ├── logging.py
│           ├── colors.py
│           └── path.py
├── tests/                       # Unit tests
├── schemas/                     # JSON schema definitions
├── config/                      # Configuration files
├── data/                        # Output directory
├── pyproject.toml              # Project metadata
├── setup.py                    # Setup script
└── README.md

## Documentation

### 1. Schema Definition

Schemas are defined using [JSON Schema](https://json-schema.org/) with MongoDB BSON type extensions.

#### Schema Properties

- `name` (optional): Name for this schema. Defaults to filename.
- `count` (optional): Number of documents to generate. Default: 1
- `$jsonSchema` (required): JSON Schema definition with BSON types

#### Example Schema

```json
{
  "name": "products",
  "count": 50,
  "$jsonSchema": {
    "properties": {
      "product_id": {
        "bsonType": "objectId",
        "description": "#object_id()#"
      },
      "name": {
        "bsonType": "string",
        "description": "#catch_phrase()#"
      },
      "price": {
        "bsonType": "decimal",
        "description": "#random_int(10, 1000)#"
      },
      "in_stock": {
        "bsonType": "bool",
        "description": "#boolean()#"
      },
      "tags": {
        "bsonType": "array",
        "minItems": 1,
        "maxItems": 5,
        "items": {
          "bsonType": "string",
          "description": "#word()#"
        }
      }
    }
  }
}
```

### 2. Supported BSON Types

|        Type        | Number |   Alias    | Supported |
| :----------------: | :----: | :--------: | :-------: |
|       Double       |   1    |   double   |  ✅  |
|       String       |   2    |   string   |  ✅  |
|       Object       |   3    |   object   |  ✅  |
|       Array        |   4    |   array    |  ✅  |
|    Binary data     |   5    |  binData   |  ✅  |
|      ObjectId      |   7    |  objectId  |  ✅  |
|      Boolean       |   8    |    bool    |  ✅  |
|        Date        |   9    |    date    |  ✅  |
|        Null        |   10   |    null    |  ✅  |
| Regular Expression |   11   |   regex    |  ❌  |
|     JavaScript     |   13   | javascript |  ❌  |
|   32-bit integer   |   16   |    int     |  ✅  |
|     Timestamp      |   17   | timestamp  |  ❌  |
|   64-bit integer   |   18   |    long    |  ✅  |
|     Decimal128     |   19   |  decimal   |  ✅  |
|      Min key       |   -1   |   minKey   |  ❌  |
|      Max key       |  127   |   maxKey   |  ❌  |

### 3. Value Generation

Use the `description` field to specify how values should be generated using Faker methods.

#### Format

```
#<method_name>(<param1>, <param2>, ...)#
```

#### Examples

- `#name()#` - Generate a random name
- `#email()#` - Generate a random email
- `#random_int(18, 80)#` - Random integer between 18 and 80
- `#date_of_birth(None, 18, 25)#` - Random birthday, age 18-25
- `#sentence(50)#` - Random sentence with 50 words
- `#uuid4()#` - Generate UUID

See [Faker Standard Providers](https://faker.readthedocs.io/en/stable/providers.html) for all available methods.

#### Using Enums

Use standard JSON Schema `enum` for predefined values:

```json
{
  "status": {
    "bsonType": "string",
    "enum": ["pending", "active", "completed", "cancelled"]
  }
}
```

### 4. Output Providers

Configure output destinations in `config/config.json`:

#### EJSON File Provider

```json
{
  "output": {
    "ejson": {
      "folder": "data"
    }
  }
}
```

Output files are saved as `{schema_name}.ejson` in the specified folder.

#### MongoDB Provider

```json
{
  "output": {
    "mongodb": {
      "uri": "mongodb://localhost:27017/mydb",
      "batch_size": 1000
    }
  }
}
```

- `uri` (required): MongoDB connection string
- `batch_size` (optional): Number of documents per batch insert (default: 1000)

#### Kafka Provider

```json
{
  "output": {
    "kafka": {
      "bootstrap_servers": "localhost:9092"
    }
  }
}
```

- `bootstrap_servers` (required): Kafka server address
- Topic name is derived from schema name

#### Multiple Outputs

You can enable multiple providers simultaneously:

```json
{
  "output": {
    "ejson": { "folder": "data" },
    "mongodb": { "uri": "mongodb://localhost:27017/mydb" },
    "kafka": { "bootstrap_servers": "localhost:9092" }
  }
}
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/mockdata.git
cd mockdata

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=mockdata --cov-report=html

# Run specific test file
pytest tests/test_mock_data.py
```

### Code Quality

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Lint code
flake8 src tests

# Type checking
mypy src
```

## Environment Variables

- `LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

```bash
LOG_LEVEL=DEBUG mockdata
```

## Examples

See the `schemas/` directory for example schema definitions:
- [fruit.json](schemas/fruit.json) - Simple schema with enums
- [scores.json](schemas/scores.json) - Complex schema with nested objects

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on top of [Faker](https://faker.readthedocs.io/) library
- Supports [MongoDB Extended JSON](https://www.mongodb.com/docs/manual/reference/mongodb-extended-json/)
- Uses [JSON Schema](https://json-schema.org/) for data structure definition

## Changelog

### Version 0.2.0 (Current)

- 🏗️ **Project restructuring**: Reorganized codebase following Python best practices
  - Moved code to `src/mockdata/` package structure
  - Separated core logic, providers, and utilities into distinct modules
  - Added comprehensive type hints and docstrings
- 📦 **Modern packaging**: Added `pyproject.toml` for modern Python packaging
- ✅ **Testing framework**: Added pytest-based test suite with coverage
- 📚 **Improved documentation**: Enhanced README with detailed examples
- 🔧 **Better configuration**: Moved config to `config/` directory
- 🎯 **CLI improvements**: Better error handling and user feedback
- 🐛 **Bug fixes**: Various improvements to reliability and error messages

### Version 0.1.0

- Initial release with basic mock data generation
- Support for EJSON, MongoDB, and Kafka outputs
- JSON Schema-based data definition
