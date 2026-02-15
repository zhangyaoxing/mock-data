"""Command-line interface for mock data generator."""

import os
import sys
import json

from mockdata.core.mock_data import MockData
from mockdata.providers import EJsonProvider, MongoDBProvider, KafkaProvider
from mockdata.utils import load_config, get_logger, cyan, green, bold
from mockdata.utils.path import get_project_path


logger = get_logger(__name__)


def read_schemas() -> dict:
    """Read all JSON schema files from the schemas directory.

    Returns:
        Dictionary with filenames as keys and schema content as values.
    """
    logger.info(cyan("Reading schema definition files from the schemas directory."))
    schemas = {}
    schemas_path = get_project_path("schemas")

    if not schemas_path.exists():
        logger.error("Schemas directory not found: %s", schemas_path)
        return schemas

    for filename in os.listdir(schemas_path):
        if filename.endswith(".json"):
            file_path = schemas_path / filename
            logger.info("Loading: %s", cyan(filename))
            with open(file_path, "r", encoding="utf-8") as file:
                schemas[filename] = json.load(file)

    logger.info(bold(green(f"All schemas loaded successfully. ({len(schemas)} schemas)")))
    return schemas


def add_providers(mock_data: MockData, config: dict) -> None:
    """Add output providers to MockData instance based on configuration.

    Args:
        mock_data: MockData instance to add providers to.
        config: Configuration dictionary containing output provider settings.
    """
    output_provider_config = config.get("output", {})

    if "ejson" in output_provider_config:
        mock_data.add_provider(EJsonProvider(output_provider_config["ejson"]))

    if "mongodb" in output_provider_config:
        mock_data.add_provider(MongoDBProvider(output_provider_config["mongodb"]))

    if "kafka" in output_provider_config:
        mock_data.add_provider(KafkaProvider(output_provider_config["kafka"]))


def show_progress(current: int, total: int) -> None:
    """Display progress indicator.

    Args:
        current: Current progress count.
        total: Total count for completion.
    """
    spinner = ["|", "/", "-", "\\"]
    percentage = round(current / total * 100, 2) if total > 0 else 0
    sys.stdout.write(f"\r{spinner[current % len(spinner)]} {percentage}%")
    sys.stdout.flush()


def main() -> None:
    """Main entry point for the CLI."""
    try:
        config = load_config()
        schemas = read_schemas()

        if not schemas:
            logger.error("No schemas found. Please add JSON schema files to the schemas directory.")
            sys.exit(1)

        logger.info(cyan("Mocking data based on the provided schemas."))

        for name, schema in schemas.items():
            schema["name"] = schema.get("name", name)
            mock_data = MockData(schema)
            add_providers(mock_data, config)

            processed_count = 0
            for _ in mock_data.run():
                processed_count += 1
                show_progress(processed_count, mock_data.count)

            mock_data.close()

            # Clear progress line
            sys.stdout.write("\r")
            sys.stdout.flush()

            logger.info(
                bold(
                    green(
                        f"Successfully mocked {processed_count} objects for schema: {schema['name']}"
                    )
                )
            )

    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user.")
        sys.exit(1)


if __name__ == "__main__":
    main()
