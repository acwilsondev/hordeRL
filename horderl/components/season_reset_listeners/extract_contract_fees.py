import random
from typing import List

from horderl.components.events.delete_event import Delete
from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)
from horderl.components.tax_value import TaxValue
from horderl.engine import palettes
from horderl.i18n import t


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
            scene.warn(t("warning.contract_quitters"))
        if contract_fees > 0:
            scene.message(
                t("message.contract_fees", amount=contract_fees),
                color=palettes.GOLD,
            )
            scene.gold -= contract_fees
