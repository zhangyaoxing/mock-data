from datetime import date, datetime
from multiprocessing import get_logger
from bson import Binary, ObjectId
from faker import Faker
from libs.providers.output_provider import OutputProvider
from libs.utils import *
from libs.object_id_provider import ObjectIdProvider
import re
import sys
import uuid

class MockData:
    def __init__(self, schema: dict):
        self._fake = Faker()
        self._fake.add_provider(ObjectIdProvider)
        self._schema = schema
        self._count = self._schema.get("count", 1)
        self._name = self._schema.get('name', f'{self._fake.slug()}')
        self._logger = get_logger(__name__)
        self._exp_pattern = re.compile(r"\#(\w+)(?:\((.*?)\))?\#")
        self._output_providers = []

    def add_provider(self, provider):
        """
        Add a custom provider to the Faker instance.
        """
        if not isinstance(provider, OutputProvider):
            self._logger.fatal(red(f"Provider {provider} is not an instance of BaseProvider."))
            sys.exit(1)
        provider.set_name(self._name)
        self._output_providers.append(provider)

    def run(self):
        """
        Mock data based on the provided schema name and data.
        The function will be called recursively for nested schemas.
        """
        self._logger.info(f"Processing schema: {cyan(self._name)}")

        def get_result():
            result = self._mock_fields(self._schema.get("$jsonSchema", {}).get("properties", {}))
            for provider in self._output_providers:
                provider.write(result)
            return result

        for _ in range(self._count):
            yield get_result()
    
    def close(self):
        """
        Close all output providers.
        """
        for provider in self._output_providers:
            provider.close()

    def _mock_fields(self, properties):
        """
        Mock data for a single field based on its schema.
        """
        obj = {}
        for field_name, field_schema in properties.items():
            bson_type = field_schema.get("bsonType", None)
            enum = field_schema.get("enum", None)
            if not bson_type:
                self._logger.fatal(red(f"Field {field_name} has no bsonType defined."))
                sys.exit(1)
            if bson_type != "object" and bson_type != "array":
                description = field_schema.get("description", None)
                if description:
                    value_desc = self._resolve_description(description)
                    gen_method = getattr(self._fake, value_desc["gen_method"], None)
                    if not gen_method:
                        self._logger.fatal(red(f"Generator method {value_desc['gen_method']} not found for field {field_name}."))
                        sys.exit(1)
                    value = gen_method(*value_desc["params"])
                elif enum:
                    if not isinstance(enum, list) or len(enum) == 0:
                        self._logger.fatal(red(f"Enum for field {field_name} must be a non-empty list."))
                        sys.exit(1)
                    value = self._fake.random_element(elements=enum)
                else:
                    self._logger.fatal(red(f"Field {field_name} has no description or enum defined."))
                    sys.exit(1)
            match bson_type:
                case "double":
                    try:
                        converted_value = float(value)
                    except ValueError:
                        self._logger.fatal(red(f"Expected float for field {field_name}, got {type(value)}."))
                        sys.exit(1)
                case "string":
                    converted_value = str(value)
                case "binData":
                    match value_desc["gen_method"]:
                        case "uuid4":
                            try:
                                u = uuid.UUID(value)
                                converted_value = Binary(u.bytes, u.version)
                            except ValueError:
                                self._logger.fatal(red(f"Expected UUID for field {field_name}, got {type(value)}."))
                                sys.exit(1)
                case "objectId":
                    if isinstance(value, ObjectId):
                        converted_value = value
                    else:
                        self._logger.fatal(red(f"Expected ObjectId for field {field_name}, got {type(value)}."))
                        sys.exit(1)
                case "bool":
                    converted_value = bool(value)
                case "date":
                    if isinstance(value, date):
                        converted_value = datetime.combine(value, datetime.min.time())
                    elif isinstance(value, datetime):
                        converted_value = value
                    else:
                        self._logger.fatal(red(f"Expected datetime for field {field_name}, got {type(value)}."))
                        sys.exit(1)
                case "int":
                    try:
                        converted_value = int(value)
                        if converted_value < -2**31 or converted_value > 2**31 - 1:
                            self._logger.fatal(red(f"Expected 32-bit integer for field {field_name}, got {converted_value}."))
                            sys.exit(1)
                    except ValueError:
                        self._logger.fatal(red(f"Expected int for field {field_name}, got {type(value)}."))
                        sys.exit(1)
                case "long":
                    try:
                        converted_value = int(value)
                    except ValueError:
                        self._logger.fatal(red(f"Expected long for field {field_name}, got {type(value)}."))
                        sys.exit(1)
                case "decimal":
                    try:
                        converted_value = float(value)
                    except ValueError:
                        self._logger.fatal(red(f"Expected decimal for field {field_name}, got {type(value)}."))
                        sys.exit(1)
                case "object":
                    sub_properties = field_schema.get("properties", {})
                    converted_value = self._mock_fields(sub_properties)
                case "array":
                    # TODO: the json schema allows multi-schemas for array items, handle this case
                    item_schema = field_schema.get("items", {})
                    min_items = field_schema.get("minItems", 0)
                    max_items = field_schema.get("maxItems", 5)
                    item_count = self._fake.random_int(min=min_items, max=max_items)
                    items = []
                    for _ in range(item_count):
                        item_value = self._mock_fields({"item": item_schema})
                        items.append(item_value["item"])
                    converted_value = items
                case _:
                    self._logger.fatal(red(f"Unsupported bsonType {bson_type} for field {field_name}."))
                    sys.exit(1)
            obj[field_name] = converted_value
        return obj

    def _resolve_description(self, description):
        """
        Resolve the description to a more readable format.
        """
        matched = self._exp_pattern.search(description)
        if not matched:
            self._logger.fatal(yellow(f"Invalid description format: {description}"))
            sys.exit(1)
        gen_method = matched.group(1) if matched else "text"
        params_str = matched.group(2) if matched else None
        params = params_str.split(",") if params_str != "" and params_str is not None else []
        converted_params = []

        # TODO: Handle more complex parameter types
        for param in params:
            param = param.strip().lower()
            if param.isdigit():
                converted_params.append(int(param))
            elif re.match(r"^\d+\.\d+$", param):
                converted_params.append(float(param))
            elif param == "true" or param == "false":
                converted_params.append(True if param == "true" else False)
            elif param == "null" or param == "none":
                converted_params.append(None)
            elif re.match(r"^\'(.*)\'$", param):
                converted_params.append(re.match(r"^\'(.*)\'$", param).group(1))
            elif re.match(r'^"(.*)"$', param):
                converted_params.append(re.match(r'^"(.*)"$', param).group(1))
            else:
                converted_params.append(param)

        return {
            "gen_method": gen_method,
            "params": converted_params
        }