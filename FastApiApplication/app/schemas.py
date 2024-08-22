from pydantic import BaseModel
from typing import Optional

class CustomerSchema(BaseModel):
    id: int
    external_id: str
    name: str
    email: str

    class Config:
        orm_mode = True

class CampaignSchema(BaseModel):
    id: int
    external_id: str
    name: str
    details: Optional[dict]

    class Config:
        orm_mode = True
