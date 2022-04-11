import uuid
from datetime import datetime
from random import randint

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


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
    creator_network = db.Column(db.String(20),)
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


@app.route('/nft-api/v1/mint', methods=['POST'])
def mint():
    new_nft = NFT()
    db.session.add(new_nft)
    db.session.commit()
    return f'Created NFT with asset id: {new_nft.asset_id}', 201, {'location': f'/nft-api/v1/NFT/{new_nft.asset_id}'}


@app.route('/nft-api/v1/NFT/all', methods=['GET'])
def get_all_nft():
    return jsonify([nft2.to_dict() for nft2 in NFT.query.order_by(NFT.date_of_creation).all()])


@app.route('/nft-api/v1/NFT/<string:asset_id>', methods=['GET'])
def get_nft(asset_id):
    retrieved_element = NFT.query.filter_by(asset_id=asset_id).first()
    return jsonify(retrieved_element.to_dict()) if retrieved_element else "NFT Not found"


@app.errorhandler(500)
def serverError():
    return "A server error: contact administrator"


@app.errorhandler(404)
def pageNotFound(e):
    return "Notification: The page was not found"


if __name__ == '__main__':
    app.run(debug=True)