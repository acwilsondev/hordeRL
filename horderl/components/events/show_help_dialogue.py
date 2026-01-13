from engine.components import EnergyActor
from horderl.gui.help_dialogue import HelpDialogue
from horderl.i18n import t


class ShowHelpDialogue(EnergyActor):
    def act(self, scene) -> None:
        messages = [
            t("help.dialogue.intro"),
            t("help.dialogue.controls"),
            t("help.dialogue.money"),
            t("help.dialogue.money_pt2"),
            t("help.dialogue.attacks"),
        ]
        if hasattr(scene, "message"):
            for message in messages:
                scene.message(message)
        scene.add_gui_element(HelpDialogue(messages, scene.config))
        scene.cm.delete_component(self)
