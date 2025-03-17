from dataclasses import dataclass
from typing import List

from horderl.components.season_reset_listeners.seasonal_actor import \
    SeasonResetListener
from horderl.components.tax_value import TaxValue
from horderl.engine import palettes


@dataclass
class CollectTaxes(SeasonResetListener):
    def on_season_reset(self, scene, season):
        self._log_debug("collecting taxes from the village")
        taxes: List[TaxValue] = scene.cm.get(TaxValue, query=lambda tv: tv.value > 0)
        collected_taxes = sum(tax.value for tax in taxes)
        scene.message(
            f"You collect {collected_taxes}c from the village.", color=palettes.GOLD
        )
        scene.gold += collected_taxes
