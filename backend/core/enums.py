from __future__ import annotations
from enum import Enum

class State(str, Enum):
    TX = "TX"
    NY = "NY"
    CA = "CA"
    FL = "FL"
    MI = "MI"
    IL = "IL"

class PropertyType(str, Enum):
    COMMUNITY = "community"
    SEPARATE = "separate"