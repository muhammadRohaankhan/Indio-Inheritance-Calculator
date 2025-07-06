from core.enums import State
from pydantic import BaseModel, Field, validator
from datetime import date
from typing import List, Optional, Dict

class PersonIn(BaseModel):
    name: str
    is_alive: bool = True
    is_step: bool = False
    is_adopted: bool = False
    children: List["PersonIn"] = []

    class Config:
        orm_mode = True

PersonIn.update_forward_refs()

class EstateInput(BaseModel):
    state: State
    date_of_death: date
    has_will: bool = False
    total_estate: float = Field(..., gt=0)

    # spouse
    spouse_exists: bool = False
    # property breakdown (community vs separate)
    community_estate: Optional[float] = None  # if None, assume all separate

    # descendants tree (children of decedent)
    children: List[PersonIn] = []

    # parents / siblings flags (needed for some states)
    parents_alive: bool = False
    siblings_alive: bool = False

    # rudimentary validation
    @validator("community_estate", always=True)
    def validate_community(cls, v, values):
        if values.get("state") in {State.TX, State.CA} and v is None:
            # assume half of total for quick default
            return values["total_estate"]/2
        return v

class EstateDistribution(BaseModel):
    distribution: Dict[str, float]