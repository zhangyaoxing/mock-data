from mockdata.utils.simple_ai import SimpleAI


def test_simple_ai():
    ai = SimpleAI()
    result = ai.guess("personal_email", "string")
    assert result == "free_email"

    result = ai.guess("birthdate", "date")
    assert result == "date_of_birth"

    result = ai.guess("username", "string")
    assert result == "name"

    result = ai.guess("objId", "objectId")
    assert result == "object_id"

    result = ai.guess("created_at", "date")
    assert result == "date_time"

    result = ai.guess("length", "decimal")
    assert result == "pyint"

    result = ai.guess("is_active", "bool")
    assert result in ["boolean", "null_boolean"]

    result = ai.guess("uuid", "string")
    assert result == "uuid4"
