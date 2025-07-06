from core.calculator_base import BaseInheritanceCalculator
from core.models import EstateInput

class MichiganCalculator(BaseInheritanceCalculator):
    def spouse_share(self, data: EstateInput):
        if not data.spouse_exists:
            return data.total_estate, {}
        spouse_portion = 0
        remaining = data.total_estate

        pref = 150000
        spouse_portion += min(pref, remaining)
        remaining -= min(pref, remaining)

        if data.children or data.parents_alive:
            spouse_portion += remaining / 2
            remaining /= 2
        else:
            spouse_portion += remaining
            remaining = 0

        return remaining, {"Spouse": spouse_portion}
