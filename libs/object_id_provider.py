from faker.providers import BaseProvider
from bson import ObjectId

class ObjectIdProvider(BaseProvider):
    def object_id(self) -> ObjectId:
        return ObjectId()