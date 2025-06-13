from autogen_core._serialization import JSON_DATA_CONTENT_TYPE, MessageSerializer

class StringMessageSerializer(MessageSerializer[str]):
    """Serialize plain strings as UTF-8 JSON text."""

    @property
    def data_content_type(self) -> str:
        return JSON_DATA_CONTENT_TYPE

    @property
    def type_name(self) -> str:
        return "str"

    def deserialize(self, payload: bytes) -> str:
        return payload.decode("utf-8")

    def serialize(self, message: str) -> bytes:
        return message.encode("utf-8")
