import sys, os; sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import datetime
from core.enums import State
from core.models import EstateInput, PersonIn
from states import REGISTRY
from api.routes import _build_person


def test_calculators_basic():
    for state in State:
        data = EstateInput(
            state=state,
            date_of_death=datetime.date(2024, 1, 1),
            total_estate=1000.0,
            spouse_exists=False,
            community_estate=500.0 if state in {State.TX, State.CA} else None,
            children=[],
        )
        calc = REGISTRY[state]
        result = calc.calculate(data)
        assert isinstance(result, dict)
        assert sum(result.values()) <= data.total_estate


def test_stepchild_excluded():
    data = EstateInput(
        state=State.IL,
        date_of_death=datetime.date(2024, 1, 1),
        total_estate=1000.0,
        spouse_exists=False,
        children=[
            PersonIn(name="Bio", is_alive=True, children=[]),
            PersonIn(name="Step", is_alive=True, is_step=True, children=[]),
        ],
    )
    calc = REGISTRY[State.IL]
    children = [_build_person(c) for c in data.children]
    data.children = children
    result = calc.calculate(data)
    assert result.get("Bio") == 1000.0
    assert "Step" not in result


def test_predeceased_child_per_stirpes():
    data = EstateInput(
        state=State.IL,
        date_of_death=datetime.date(2024, 1, 1),
        total_estate=1000.0,
        spouse_exists=False,
        children=[
            PersonIn(
                name="Child1",
                is_alive=False,
                children=[
                    PersonIn(name="G1", is_alive=True, children=[]),
                    PersonIn(name="G2", is_alive=True, children=[]),
                ],
            ),
            PersonIn(name="Child2", is_alive=True, children=[]),
        ],
    )
    calc = REGISTRY[State.IL]
    children = [_build_person(c) for c in data.children]
    data.children = children
    result = calc.calculate(data)
    assert result.get("Child2") == 500.0
    assert result.get("G1") == 250.0
    assert result.get("G2") == 250.0
