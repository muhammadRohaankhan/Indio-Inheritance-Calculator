from backend.core.tree import Person
from typing import List, Dict, Tuple

class BaseInheritanceCalculator:
    """Provide per‑stirpes distribution and spouse hooks; subclasses override shares."""

    def _has_living_desc(self, person: Person) -> bool:
        return any(
            (child.is_alive and child.eligible()) or self._has_living_desc(child)
            for child in person.children
        )

    def spouse_share(self, data: "EstateInput") -> Tuple[float, Dict[str, float]]:
        """Return (remaining_estate, {{spouse: share}})"""
        return data.total_estate, {}

    def descendants_share(self, remainder: float, dec_children: List[Person]) -> Dict[str, float]:
        """Generic per‑stirpes on remainder (may be overridden if state deviates)."""
        dist, _ = self._by_branch(remainder, dec_children)
        return dist

    # --- Core per‑stirpes recursion -----------------------------------------
    def _by_branch(self, estate: float, heirs: List[Person], depth: int = 0) -> Tuple[Dict[str, float], List[str]]:
        logs = []
        eligible = [h for h in heirs if h.eligible()]
        branches: List[Tuple[Person|None, List[Person]]] = []
        for p in eligible:
            if p.is_alive:
                branches.append((p, []))
            elif self._has_living_desc(p):
                branches.append((None, p.children))
        if not branches:
            return {}, logs
        share = estate / len(branches)
        dist: Dict[str, float] = {}
        for alive, kids in branches:
            if alive:
                dist[alive.name] = dist.get(alive.name, 0)+share
            else:
                sub, sublog = self._by_branch(share, kids, depth+1)
                for n, s in sub.items():
                    dist[n] = dist.get(n,0)+s
                logs.extend(sublog)
        return dist, logs

    # --- Public API ----------------------------------------------------------
    def calculate(self, data: "EstateInput") -> Dict[str, float]:
        if data.has_will:
            return {"per_will": data.total_estate}
        remaining, spouse_dist = self.spouse_share(data)
        descendants_dist = self.descendants_share(remaining, data.children)
        return {**spouse_dist, **descendants_dist}