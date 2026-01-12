from horderl.components.season_reset_listeners.seasonal_actor import (
    SeasonResetListener,
)
from horderl.i18n import t


class CollectTaxesForKing(SeasonResetListener):
    """
    Collect taxes from the player at the end of the year.
    """

    value: int = 25

    def on_season_reset(self, scene, season):
        if season != "Spring":
            scene.warn(t("warning.king_collects", amount=self.value))
            return

        if scene.gold < self.value:
            scene.popup_message(
                t(
                    "popup.king_collects_insufficient",
                    amount=self.value,
                    gold=scene.gold,
                )
            )
            scene.pop()
            return

        scene.gold -= self.value
        old_value = self.value
        self.value += 25
        scene.popup_message(
            t(
                "popup.king_collects_paid",
                amount=old_value,
                next_amount=self.value,
            )
        )
