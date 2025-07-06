from backend.core.calculator_base import BaseInheritanceCalculator
from backend.core.models import EstateInput

class IllinoisCalculator(BaseInheritanceCalculator):
    def spouse_share(self, data: EstateInput):
        if not data.spouse_exists:
            return data.total_estate, {}
        spouse_portion = 0
        remaining = data.total_estate

        if data.children:
            spouse_portion = remaining / 2
            remaining /= 2
        else:
            spouse_portion = remaining
            remaining = 0

        return remaining, {"Spouse": spouse_portion}
