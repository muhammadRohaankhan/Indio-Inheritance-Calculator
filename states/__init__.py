from .texas import TexasCalculator
from .new_york import NewYorkCalculator
from core.enums import State

# from .california import CaliforniaCalculator
# from .florida import FloridaCalculator
# from .michigan import MichiganCalculator
# from .illinois import IllinoisCalculator

REGISTRY = {
    State.TX: TexasCalculator(),
    State.NY: NewYorkCalculator(),
    # State.CA: CaliforniaCalculator(),
    # State.FL: FloridaCalculator(),
    # State.MI: MichiganCalculator(),
    # State.IL: IllinoisCalculator(),
}