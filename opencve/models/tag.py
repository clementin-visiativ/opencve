from opencve.extensions import db
from opencve.models import BaseModel, cves_tags

class Tag(BaseModel):
    __tablename__ : "tags"

    name = db.Column(db.String, nullable=False)

    cve = db.relationship("Cve", secondary=cves_tags)

    def __repr__(self):
        return "<Tag {}>".format(self.id)