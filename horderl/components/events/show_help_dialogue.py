from horderl.engine.components.energy_actor import EnergyActor
from horderl.i18n import t


class ShowHelpDialogue(EnergyActor):
    def act(self, scene) -> None:
        scene.popup_message(t("help.dialogue.intro"))
        scene.popup_message(t("help.dialogue.controls"))
        scene.popup_message(t("help.dialogue.money"))
        scene.popup_message(t("help.dialogue.money_pt2"))
        scene.popup_message(t("help.dialogue.attacks"))
        scene.cm.delete_component(self)
