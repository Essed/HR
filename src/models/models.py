from pydantic import BaseModel, ConfigDict
from typing import Optional, List

from src.enums import Role
from src.payments import Billing

class TunedModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class User(TunedModel):
    id: int
    username: str
    role: Optional[Role] = Role.USER
    balance: Optional[float] = Billing().zero_balance

class Employee(TunedModel):
    username: str
    role: Optional[Role] = Role.USER

class Company(TunedModel):
    name: str
    owner_id: int
    employees: Optional[List[Employee]] = list()

class Guild(TunedModel):
    company_name: str
    members: Optional[List[str]] = list()