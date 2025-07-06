from fastapi import APIRouter, HTTPException
from core.models import EstateInput, EstateDistribution
from states import REGISTRY
from core.tree import Person

router = APIRouter()

# helper to convert PersonIn → Person recursively

def _build_person(p_in):
    return Person(
        name=p_in.name,
        is_alive=p_in.is_alive,
        is_step=p_in.is_step,
        is_adopted=p_in.is_adopted,
        children=[_build_person(c) for c in p_in.children]
    )
@router.post("/calculate", response_model=EstateDistribution)
def calculate(data: EstateInput):
    calc = REGISTRY.get(data.state)
    if not calc:
        raise HTTPException(400, "State not supported yet")
    # Convert all children (and their children) to business objects
    children = [_build_person(c) for c in data.children]
    # Make a shallow copy of the Pydantic model and set children
    data_for_calc = data.copy()
    data_for_calc.children = children
    distribution = calc.calculate(data_for_calc)
    return {"distribution": distribution}
