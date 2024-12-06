import json

from uuid import UUID
from pydantic import BaseModel as _BaseModel


class BaseModel(_BaseModel):
    """The BaseModel for pydantic_api Project"""

    model_config = {
        "from_attributes": True,
        "extra": "allow",
        "json_encoders": {UUID: str},
    }

    def dump_json_dict(self) -> dict:
        return json.loads(self.model_dump_json())


__all__ = [
    "BaseModel",
]
