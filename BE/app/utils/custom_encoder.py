import json
import typing

from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__,DeclarativeMeta):
            return {col.name: getattr(obj,col.name) for col in obj.__table__.columns}
        if isinstance(obj, BaseModel):
            return obj.dict()
        if isinstance(obj, datetime):
            return obj.isoformat()

        return super().default(obj)

class ORJSONResponse(JSONResponse):
    def render(self, content: typing.Any) -> bytes:
        return json.dumps(content, cls=CustomEncoder).encode("utf-8")