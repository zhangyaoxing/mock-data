"""Custom Faker providers for mock data generation."""

from faker.providers import BaseProvider
from bson import ObjectId


class ObjectIdProvider(BaseProvider):
    """Provider for generating MongoDB ObjectIds."""

    def object_id(self) -> ObjectId:
        """Generate a new MongoDB ObjectId."""
        return ObjectId()
