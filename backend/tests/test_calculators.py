import datetime
from backend.core.enums import State
from backend.core.models import EstateInput, PersonIn
from backend.states import REGISTRY
from backend.api.routes import _build_person
import pytest


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


def test_texas_children_from_previous_marriage():
    data = EstateInput(
        state=State.TX,
        date_of_death=datetime.date(2024, 1, 1),
        total_estate=1000.0,
        spouse_exists=True,
        community_estate=600.0,
        children_from_previous_marriage=True,
        children=[
            PersonIn(name="C1", is_alive=True, children=[]),
            PersonIn(name="C2", is_alive=True, children=[]),
        ],
    )
    calc = REGISTRY[State.TX]
    children = [_build_person(c) for c in data.children]
    data.children = children
    result = calc.calculate(data)
    assert result.get("Spouse") == pytest.approx(333.33, rel=1e-2)
    assert result.get("C1") == pytest.approx(333.33, rel=1e-2)
    assert result.get("C2") == pytest.approx(333.33, rel=1e-2)


def test_texas_no_prior_children():
    data = EstateInput(
        state=State.TX,
        date_of_death=datetime.date(2024, 1, 1),
        total_estate=1000.0,
        spouse_exists=True,
        community_estate=600.0,
        children_from_previous_marriage=False,
        children=[
            PersonIn(name="C1", is_alive=True, children=[]),
            PersonIn(name="C2", is_alive=True, children=[]),
        ],
    )
    calc = REGISTRY[State.TX]
    children = [_build_person(c) for c in data.children]
    data.children = children
    result = calc.calculate(data)
    assert result.get("Spouse") == pytest.approx(533.33, rel=1e-2)
    assert result.get("C1") == pytest.approx(233.33, rel=1e-2)
    assert result.get("C2") == pytest.approx(233.33, rel=1e-2)
