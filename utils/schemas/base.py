from typing import Optional

from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: Optional[str]
    created_by: Optional[str]
    updated_by: Optional[str]
    is_deleted: Optional[bool] = False
