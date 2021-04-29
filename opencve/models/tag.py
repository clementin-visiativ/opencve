from opencve.extensions import db
from opencve.models import BaseModel

class Tag(BaseModel):
    __tablename__ : "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<Tag {}>".format(self.id)