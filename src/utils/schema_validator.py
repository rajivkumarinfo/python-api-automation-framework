#Thin wrapper around jsonschema for readable, Allure-visible assertions.
import json

import allure
from jsonschema import Draft7Validator
from jsonschema.exceptions import best_match


@allure.step("Validate response against JSON schema")
def assert_matches_schema(instance: dict, schema: dict) -> None:
    #Validate `instance` against `schema`, raising a readable AssertionError.

    # Uses Draft7Validator directly (instead of jsonschema.validate) so that we can report the single most relevant error via `best_match`, which is far
    # more actionable in a CI log / Allure report than the default traceback.

    validator = Draft7Validator(schema)
    errors = list(validator.iter_errors(instance))

    if errors:
        error = best_match(errors)
        allure.attach(
            json.dumps(instance, indent=2, default=str),
            name="Payload that failed schema validation",
            attachment_type=allure.attachment_type.JSON,
        )
        raise AssertionError(
            f"Schema validation failed at '{'/'.join(str(p) for p in error.path)}': "
            f"{error.message}"
        )
