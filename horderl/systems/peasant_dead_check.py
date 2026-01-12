from ..components.tags.peasant_tag import PeasantTag
from ..i18n import t


def run(scene):
    faction_members = scene.cm.get(PeasantTag)
    if not faction_members:
        scene.popup_message(
            t("message.peasants_dead")
        )
        scene.pop()
