from core.calculator_base import BaseInheritanceCalculator
from core.models import EstateInput

class CaliforniaCalculator(BaseInheritanceCalculator):
    def spouse_share(self, data: EstateInput):
        if not data.spouse_exists:
            return data.total_estate, {}
        spouse_portion = 0
        remaining = data.total_estate

        # Community property: spouse already owns half. If all children are shared,
        # spouse inherits decedent's half as well.
        community_half = data.community_estate / 2 if data.community_estate else 0
        if data.children and all(child.is_step is False for child in data.children):
            spouse_portion += community_half
            remaining -= community_half

        # Separate property rules (simplified)
        child_count = len(data.children)
        if child_count == 0:
            spouse_portion = data.total_estate
            remaining = 0
        elif child_count == 1:
            spouse_portion += remaining / 2
            remaining /= 2
        else:
            spouse_portion += remaining / 3
            remaining *= 2/3

        return remaining, {"Spouse": spouse_portion}
