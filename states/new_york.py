from core.calculator_base import BaseInheritanceCalculator
from core.models import EstateInput


class NewYorkCalculator(BaseInheritanceCalculator):
    def spouse_share(self, data: EstateInput):
        if not data.spouse_exists:
            return data.total_estate, {}
        pref = 50000
        spouse_portion = 0
        remaining = data.total_estate
        if data.children:
            spouse_portion += min(pref, remaining)
            remaining -= spouse_portion
            spouse_portion += remaining/2
            remaining /= 2
        else:
            spouse_portion = data.total_estate
            remaining = 0
        return remaining, {"Spouse": spouse_portion}
