from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple

@dataclass
class Person:
    name: str
    is_alive: bool = True
    is_step: bool = False
    is_adopted: bool = False
    children: List["Person"] = field(default_factory=list)

    # helper
    def eligible(self) -> bool:
        return not (self.is_step and not self.is_adopted)
