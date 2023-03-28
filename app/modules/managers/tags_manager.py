from ..models.base import db
from ..models.tags import Tag


class TagsManager:
    @staticmethod
    def save_tag(tag: Tag):
        db.session.add(tag)
        db.session.commit()
