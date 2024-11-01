from pydantic import BaseModel, ConfigDict

class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class User(TunedModel):
    id: int
    username: str   