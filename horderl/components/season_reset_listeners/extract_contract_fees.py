import random
from typing import List

from horderl.components.events.delete_event import Delete
from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)
from horderl.components.tax_value import TaxValue
from horderl.engine import palettes


class ExtractContractFees(SeasonResetListener):
    def on_season_reset(self, scene, season):
        self._log_debug("extracting contract fees")
        taxes: List[TaxValue] = scene.cm.get(
            TaxValue, query=lambda tv: tv.value < 0
        )
        contract_fees = -1 * sum(tax.value for tax in taxes)

        if contract_fees == 0:
            return

        quitters = False
        while scene.gold < contract_fees:
            quitters = True
            random.shuffle(taxes)
            quitter = taxes.pop().entity
            scene.cm.add(Delete(entity=quitter))
            contract_fees = -1 * sum(tax.value for tax in taxes)

        if quitters:
            scene.warn(
                f"Several mercenaries abandoned you, because you could not pay"
                f" them."
            )
        if contract_fees > 0:
            scene.message(
                f"You racked up {contract_fees}c in contract fees.",
                color=palettes.GOLD,
            )
            scene.gold -= contract_fees
