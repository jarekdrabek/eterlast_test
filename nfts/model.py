import uuid
from datetime import datetime
from random import randint

from sqlalchemy_serializer import SerializerMixin

from nfts import db


class User(db.Model, SerializerMixin):
    serialize_only = ('address')
    address = db.Column(db.String, primary_key=True)

    def __repr__(self):
        return f'User(user_wallet_address="{self.id}")'


def generate_uuid():
    return str(uuid.uuid4())


class Collection(db.Model, SerializerMixin):
    serialize_only = ('id', 'name', 'description', 'creator', 'creator_network')

    id = db.Column(db.String, primary_key=True, default=generate_uuid)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text(120))
    creator = db.Column(db.Integer, db.ForeignKey('user.address'), nullable=False )
    creator_network = db.Column(db.String(20))
    nfts = db.relationship('NFT', backref='collection')

    def __repr__(self):
        return f'Collection("{self.name}" [created by "{self.creator}" on network "{self.creator_network}"])'


def generate_16char_hex():
    return hex(randint(0, 2**64))


class NFT(db.Model, SerializerMixin):
    serialize_only = ('asset_id', 'name', 'picture', 'external_link', 'description', 'supply', 'royalties', 'date_of_creation', 'buyer')

    asset_id = db.Column(db.String(16), primary_key=True, default=generate_16char_hex)
    name = db.Column(db.String(20), nullable=False, default='name_to_change')
    picture = db.Column(db.String(120))
    external_link = db.Column(db.String(120))
    description = db.Column(db.Text(120))
    collection_id = db.Column(db.String(16), db.ForeignKey('collection.id'))

    supply = db.Column(db.Integer)
    royalties = db.Column(db.Integer)
    date_of_creation = db.Column(db.DateTime, default=datetime.utcnow)
    buyer = db.Column(db.String)

    def __repr__(self):
        return f'NFT(id="{self.asset_id}", name="{self.name}")'