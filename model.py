import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from flask_sqlalchemy import SQLAlchemy

from nfts import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    address = db.Column(db.String, primary_key=True)

    def __repr__(self):
        return f'User(user_wallet_address="{self.id}")'


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text(120))
    creator = db.Column(db.Integer, db.ForeignKey('user.address'), nullable=False )
    creator_network = db.Column(db.String(20),)
    nfts = db.relationship('NFT', backref='collection')

    def __repr__(self):
        return f'Collection("{self.name}" [created by "{self.creator}" on network "{self.creator_network}"])'


class NFT(db.Model):
    asset_id = db.Column(db.String(16), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    picture = db.Column(db.String(120))
    external_link = db.Column(db.String(120))
    description = db.Column(db.Text(120))
    collection_id = db.Column(db.String(16), db.ForeignKey('collection.id'), nullable=False)

    supply = db.Column(db.Integer)
    royalties = db.Column(db.Integer)
    date_of_creation = db.Column(db.DateTime, default=datetime.utcnow)
    buyer = db.Column(db.String)

    def __repr__(self):
        return f'NFT(id="{self.id}", name="{self.name}")'
