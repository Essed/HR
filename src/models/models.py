from pydantic import BaseModel, ConfigDict
from typing import Optional

from src.enums import Role

class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class User(TunedModel):
    id: int
    username: str
    role: Optional[Role] = Role.USER