from ..components.tags.tag import Tag, TagType
from ..i18n import t


def run(scene):
    faction_members = scene.cm.get(
        Tag, query=lambda tag: tag.tag_type == TagType.PEASANT
    )
    if not faction_members:
        scene.popup_message(t("message.peasants_dead"))
        scene.pop()
