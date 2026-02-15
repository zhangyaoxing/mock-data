"""Core MockData class for generating mock data based on JSON schemas."""

import re
import sys
import uuid
from datetime import date, datetime
from decimal import Decimal

from bson import Binary, Decimal128, ObjectId
from faker import Faker

from mockdata.core.constants import BSON_TYPES
from mockdata.core.fake_providers import ObjectIdProvider
from mockdata.providers.base import OutputProvider
from mockdata.utils.logging import get_logger
from mockdata.utils.colors import red, cyan, yellow


class MockData:
    """Main class for generating mock data based on JSON schemas."""

    def __init__(self, schema: dict):
        """Initialize MockData with a schema.

        Args:
            schema: Dictionary containing the JSON schema with count and properties.
        """
        self._fake = Faker()
        self._fake.add_provider(ObjectIdProvider)
        self._schema = schema
        self._count = self._schema.get("count", 1)
        self._name = self._schema.get("name", f"{self._fake.slug()}")
        self._logger = get_logger(__name__)
        self._exp_pattern = re.compile(r"\#(\w+)(?:\((.*?)\))?\#")
        self._output_providers = []

    def add_provider(self, provider: OutputProvider) -> None:
        """Add an output provider to the MockData instance.

        Args:
            provider: An OutputProvider instance for writing mock data.

        Raises:
            SystemExit: If provider is not an instance of OutputProvider.
        """
        if not isinstance(provider, OutputProvider):
            self._logger.fatal("Provider %s is not an instance of OutputProvider.", red(provider))
            sys.exit(1)
        provider.set_name(self._name)
        self._output_providers.append(provider)

    def run(self):
        """Generate mock data based on the schema.

        Yields:
            dict: A generated mock data object.
        """
        self._logger.info("Processing schema: %s", cyan(self._name))

        def get_result():
            result = self._mock_fields(self._schema.get("$jsonSchema", {}).get("properties", {}))
            for provider in self._output_providers:
                provider.write(result)
            return result

        for _ in range(self._count):
            yield get_result()

    def close(self) -> None:
        """Close all output providers."""
        for provider in self._output_providers:
            provider.close()

    def _mock_fields(self, properties: dict) -> dict:
        """Generate mock data for fields based on their schema.

        Args:
            properties: Dictionary of field schemas.

        Returns:
            dict: Generated mock data object.

        Raises:
            SystemExit: If field schema is invalid or type conversion fails.
        """
        obj = {}
        for field_name, field_schema in properties.items():
            bson_type = field_schema.get("bsonType", None)
            bson_type = BSON_TYPES.get(bson_type, bson_type)
            enum = field_schema.get("enum", None)

            if not bson_type:
                self._logger.fatal("Field %s has no bsonType defined.", red(field_name))
                sys.exit(1)

            # Generate value based on type
            if bson_type not in ["object", "array"]:
                description = field_schema.get("description", None)
                if description:
                    value_desc = self._resolve_description(description)
                    gen_method = getattr(self._fake, value_desc["gen_method"], None)
                    if not gen_method:
                        self._logger.fatal(
                            "Generator method %s not found for field %s.",
                            red(value_desc["gen_method"]),
                            red(field_name),
                        )
                        sys.exit(1)
                    value = gen_method(*value_desc["params"])
                elif enum:
                    if not isinstance(enum, list) or len(enum) == 0:
                        self._logger.fatal(
                            "Enum for field %s must be a non-empty list.", red(field_name)
                        )
                        sys.exit(1)
                    value = self._fake.random_element(elements=enum)
                else:
                    self._logger.fatal(
                        "Field %s has no description or enum defined.", red(field_name)
                    )
                    sys.exit(1)
            else:
                value = None

            # Convert value based on BSON type
            converted_value = self._convert_value(
                bson_type,
                value,
                field_name,
                field_schema,
                value_desc if "value_desc" in locals() else None,
            )
            obj[field_name] = converted_value

        return obj

    def _convert_value(
        self, bson_type: str, value, field_name: str, field_schema: dict, value_desc: dict = None
    ):
        """Convert a value to the appropriate BSON type.

        Args:
            bson_type: Target BSON type.
            value: Value to convert.
            field_name: Name of the field (for error messages).
            field_schema: Schema definition for the field.
            value_desc: Description of value generation method.

        Returns:
            Converted value in appropriate type.

        Raises:
            SystemExit: If type conversion fails.
        """
        match bson_type:
            case "double":
                try:
                    return float(value)
                except ValueError:
                    self._logger.fatal(
                        red(f"Expected float for field {field_name}, got {type(value)}.")
                    )
                    sys.exit(1)

            case "string":
                return str(value)

            case "binData":
                if value_desc and value_desc["gen_method"] == "uuid4":
                    try:
                        u = uuid.UUID(value)
                        return Binary(u.bytes, u.version)
                    except ValueError:
                        self._logger.fatal(
                            red(f"Expected UUID for field {field_name}, got {type(value)}.")
                        )
                        sys.exit(1)

            case "objectId":
                if isinstance(value, ObjectId):
                    return value
                else:
                    self._logger.fatal(
                        red(f"Expected ObjectId for field {field_name}, got {type(value)}.")
                    )
                    sys.exit(1)

            case "bool":
                return bool(value)

            case "date":
                if isinstance(value, date):
                    return datetime.combine(value, datetime.min.time())
                elif isinstance(value, datetime):
                    return value
                else:
                    self._logger.fatal(
                        red(f"Expected datetime for field {field_name}, got {type(value)}.")
                    )
                    sys.exit(1)

            case "int":
                try:
                    converted_value = int(value)
                    if converted_value < -(2**31) or converted_value > 2**31 - 1:
                        self._logger.fatal(
                            red(
                                f"Expected 32-bit integer for field {field_name}, got {converted_value}."
                            )
                        )
                        sys.exit(1)
                    return converted_value
                except ValueError:
                    self._logger.fatal(
                        red(f"Expected int for field {field_name}, got {type(value)}.")
                    )
                    sys.exit(1)

            case "long":
                try:
                    return int(value)
                except ValueError:
                    self._logger.fatal(
                        red(f"Expected long for field {field_name}, got {type(value)}.")
                    )
                    sys.exit(1)

            case "decimal":
                try:
                    value = Decimal(str(value)) if isinstance(value, (int, float, str)) else value
                    return Decimal128(value)
                except ValueError:
                    self._logger.fatal(
                        red(f"Expected decimal for field {field_name}, got {type(value)}.")
                    )
                    sys.exit(1)

            case "object":
                sub_properties = field_schema.get("properties", {})
                return self._mock_fields(sub_properties)

            case "array":
                # TODO: Support multi-schema arrays as per JSON schema spec
                item_schema = field_schema.get("items", {})
                min_items = field_schema.get("minItems", 0)
                max_items = field_schema.get("maxItems", 5)
                item_count = self._fake.random_int(min=min_items, max=max_items)
                items = []
                for _ in range(item_count):
                    item_value = self._mock_fields({"item": item_schema})
                    items.append(item_value["item"])
                return items

            case _:
                self._logger.fatal(red(f"Unsupported bsonType {bson_type} for field {field_name}."))
                sys.exit(1)

    def _resolve_description(self, description: str) -> dict:
        """Parse description string to extract generator method and parameters.

        Args:
            description: Description string in format #method(param1,param2)#

        Returns:
            dict: Dictionary with 'gen_method' and 'params' keys.

        Raises:
            SystemExit: If description format is invalid.
        """
        matched = self._exp_pattern.search(description)
        if not matched:
            self._logger.fatal(yellow(f"Invalid description format: {description}"))
            sys.exit(1)

        gen_method = matched.group(1) if matched else "text"
        params_str = matched.group(2) if matched else None
        params = params_str.split(",") if params_str and params_str != "" else []
        converted_params = []

        # Convert parameter strings to appropriate types
        for param in params:
            param = param.strip().lower()
            if param.isdigit():
                converted_params.append(int(param))
            elif re.match(r"^\d+\.\d+$", param):
                converted_params.append(float(param))
            elif param in ("true", "false"):
                converted_params.append(param == "true")
            elif param in ("null", "none"):
                converted_params.append(None)
            elif re.match(r"^\'(.*)\'$", param):
                converted_params.append(re.match(r"^\'(.*)\'$", param).group(1))
            elif re.match(r'^"(.*)"$', param):
                converted_params.append(re.match(r'^"(.*)"$', param).group(1))
            else:
                converted_params.append(param)

        return {"gen_method": gen_method, "params": converted_params}
