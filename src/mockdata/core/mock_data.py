"""Core MockData class for generating mock data based on JSON schemas."""

import re
import sys
import uuid
from datetime import date, datetime
from decimal import Decimal
from logging import getLogger
from typing import Any, Optional, Union

from bson import Binary, Decimal128, ObjectId
from faker import Faker

from mockdata.core.constants import BSON_TYPES
from mockdata.core.fake_providers import ObjectIdProvider
from mockdata.providers.base import OutputProvider
from mockdata.utils.colors import cyan, red, yellow
from mockdata.utils.simple_ai import SimpleAI


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
        self._count: int = self._schema.get("count", 100)
        self._name: str = self._schema.get("ns", f"{self._fake.slug()}")
        self._logger = getLogger(__name__)
        self._exp_pattern = re.compile(r"\#(\w+)(?:\((.*?)\))?\#")
        self._output_providers: list[OutputProvider] = []
        self._ai = SimpleAI()

    @property
    def count(self) -> int:
        """Get the number of mock data objects to generate.

        Returns:
            int: The count of mock data objects to generate.
        """
        return self._count

    def add_output_provider(self, provider: OutputProvider) -> None:
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
            result = self._mock_fields(self._schema.get("jsonSchema", {}).get("properties", {}))
            for provider in self._output_providers:
                provider.write(result)
            return result

        for _ in range(self._count):
            yield get_result()

    def close(self) -> None:
        """Close all output providers."""
        for provider in self._output_providers:
            provider.close()

    def _mock_fields(self, properties: dict) -> dict[str, Any]:
        """Generate mock data for fields based on their schema.

        Args:
            properties: Dictionary of field schemas.

        Returns:
            dict: Generated mock data object.

        Raises:
            SystemExit: If field schema is invalid or type conversion fails.
        """
        obj: dict[str, Any] = {}
        for field_name, field_schema in properties.items():
            bson_type = field_schema.get("bsonType", None)
            if isinstance(bson_type, list):
                # If bsonType is a list, we will randomly select one type from the list for generation.
                # TODO: allow multiple types generation for the same field as per JSON schema spec.
                bson_type = self._fake.random_element(elements=bson_type)
            if bson_type not in BSON_TYPES:
                self._logger.warning(
                    "Field %s has invalid or missing bsonType: %s. Skip...",
                    yellow(field_name),
                    yellow(bson_type),
                )
                continue
            enum = field_schema.get("enum", None)

            converted_value: Any
            # Generate value based on type
            if bson_type == "object":
                sub_properties = field_schema.get("properties", {})
                converted_value = self._mock_fields(sub_properties)
            elif bson_type == "array":
                # TODO: Support multi-schema arrays as per JSON schema spec
                item_schema = field_schema.get("items", {})
                min_items = field_schema.get("minItems", 0)
                max_items = field_schema.get("maxItems", 5)
                item_count = self._fake.random_int(min=min_items, max=max_items)
                items = []
                for _ in range(item_count):
                    item_value = self._mock_fields({"item": item_schema})
                    items.append(item_value.get("item", None))
                converted_value = items
            else:
                value: Any
                if enum:
                    # Bson type enum fields should have a non-empty list of possible values.
                    # The generator will randomly select one value from the list.
                    if not isinstance(enum, list) or len(enum) == 0:
                        self._logger.fatal(
                            "Enum for field %s must be a non-empty list.", red(field_name)
                        )
                        sys.exit(1)
                    value = self._fake.random_element(elements=enum)
                else:
                    # Compass generated schemas don't have description.
                    description = field_schema.get("description", "")
                    method, params = self._resolve_description(description)
                    if not method:
                        method = self._ai.guess(field_name, bson_type)
                        # Save the guessed method back to description,
                        # so we don't have to guess again for the same field.
                        field_schema["description"] = f"#{method}#"
                    gen_method = getattr(self._fake, method, None)
                    if not gen_method:
                        self._logger.fatal(
                            "Generator method %s not found for field %s.",
                            red(method),
                            red(field_name),
                        )
                        sys.exit(1)
                    value = gen_method(*params)

                # Convert value based on BSON type
                converted_value = self._convert_value(
                    bson_type,
                    value,
                    field_name,
                    {"gen_method": method, "params": params} if method else None,
                )
            obj[field_name] = converted_value

        return obj

    def _convert_value(
        self,
        bson_type: str,
        value: Any,
        field_name: str,
        value_desc: Optional[dict] = None,
    ):
        """Convert a value to the appropriate BSON type.

        Args:
            bson_type: Target BSON type.
            value: Value to convert.
            field_name: Name of the field (for error messages).
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
                        return Binary(u.bytes, u.version)  # type: ignore
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

            case _:
                self._logger.fatal(red(f"Unsupported bsonType {bson_type} for field {field_name}."))
                sys.exit(1)

    def _resolve_description(self, description: str) -> tuple[Optional[str], list]:
        """Parse description string to extract generator method and parameters.

        Args:
            description: Description string in format #method(param1,param2)#

        Returns:
            tuple[str | None, list]: Tuple with generator method and parameters list,
            or (None, []) if description is invalid.

        Raises:
            SystemExit: If description format is invalid.
        """
        matched: Optional[re.Match[str]] = self._exp_pattern.search(description)
        if not matched:
            return None, []
        gen_method: str = matched.group(1) if matched else "text"
        params_str: Optional[str] = matched.group(2) if matched else None
        params: list[str] = params_str.split(",") if params_str and params_str != "" else []

        converted_params: list[Union[int, float, bool, None, str]] = []

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
                m = re.match(r"^\'(.*)\'$", param)
                converted_params.append(m.group(1) if m else param)
            elif re.match(r'^"(.*)"$', param):
                m = re.match(r'^"(.*)"$', param)
                converted_params.append(m.group(1) if m else param)
            else:
                converted_params.append(param)

        return gen_method, converted_params
