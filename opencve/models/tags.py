from opencve.extensions import db
from opencve.models import BaseModel, cves_tags
from sqlalchemy_utils import UUIDType

class Tag(BaseModel):
    __tablename__ = "tags"

    name = db.Column(db.String(), nullable=False)

    user_id = db.Column(UUIDType(binary=False), db.ForeignKey("users.id"))

    def __repr__(self):
        return "<Tag {}>".format(self.name)