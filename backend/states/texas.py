from backend.core.calculator_base import BaseInheritanceCalculator
from backend.core.models import EstateInput


class TexasCalculator(BaseInheritanceCalculator):
    def spouse_share(self, data: EstateInput):
        if not data.spouse_exists:
            return data.total_estate, {}
        #  --- Simplified rule set ---
        # Community: spouse already owns 1/2. If no children from a prior relationship,
        # spouse inherits decedent's half. Otherwise decedent's half passes to children.
        spouse_portion = 0
        remaining = data.total_estate

        # community slice handling
        community_half = data.community_estate / 2 if data.community_estate else 0
        if not data.children_from_previous_marriage:
            spouse_portion += community_half  # inherits decedent half
            remaining -= community_half
        # separate property (simplified – real law splits personal vs real, life estate vs fee)
        if data.children:
            spouse_portion += remaining * (1/3)
            remaining *= (2/3)
        else:
            spouse_portion = data.total_estate
            remaining = 0
        return remaining, {"Spouse": spouse_portion}