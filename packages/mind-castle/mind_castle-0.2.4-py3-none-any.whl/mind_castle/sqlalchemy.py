import json
import logging

from sqlalchemy import types

from mind_castle.stores import get_secret, put_secret

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


class SecretData(types.TypeDecorator):
    """A sqlalchemy field type that stores data in a secret store."""

    impl = types.JSON  # The base data type for this field
    cache_ok = True

    def __init__(self, store_type: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret_type = store_type

    def process_bind_param(self, value, dialect):
        # Don't waste time storing empty values
        if value is None or value == "" or value == {} or value == []:
            return value

        # Make a string out of whatever object we got
        stringValue = json.dumps(value)

        secret_params = put_secret(stringValue, self.secret_type)
        logger.debug(f"Stored secret with: {secret_params}")
        return secret_params

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        secret_details = json.loads(value) if isinstance(value, str) else value

        if secret_details.get("secret_type") is None:
            logger.debug(
                f"No secret type found in '{secret_details}', must be a plaintext value."
            )
            return secret_details

        logger.debug(f"Restoring {secret_details} from a secret.")
        return json.loads(get_secret(secret_details))
