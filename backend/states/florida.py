from backend.core.calculator_base import BaseInheritanceCalculator
from backend.core.models import EstateInput

class FloridaCalculator(BaseInheritanceCalculator):
    def spouse_share(self, data: EstateInput):
        if not data.spouse_exists:
            return data.total_estate, {}
        spouse_portion = 0
        remaining = data.total_estate

        # If all descendants are also descendants of the spouse, spouse inherits all
        if not data.children or all(child.is_step is False for child in data.children):
            spouse_portion = data.total_estate
            remaining = 0
        else:
            spouse_portion = remaining / 2
            remaining /= 2

        return remaining, {"Spouse": spouse_portion}
