from flask import jsonify, request
from sqlalchemy import desc

from nfts import app, db
from nfts.model import NFT


@app.route('/nft-api/v1/mint', methods=['POST'])
def mint():
    data = dict(request.form)
    new_nft = NFT(**data)
    db.session.add(new_nft)
    db.session.commit()
    return f'Created NFT with asset id: {new_nft.asset_id}', 201, {'location': f'/nft-api/v1/NFT/{new_nft.asset_id}'}


@app.route('/nft-api/v1/NFT/all', methods=['GET'])
def get_all_nft():
    return jsonify([nft2.to_dict() for nft2 in NFT.query.order_by(desc(NFT.date_of_creation)).all()])


@app.route('/nft-api/v1/NFT/<string:asset_id>', methods=['GET'])
def get_nft(asset_id):
    retrieved_element = NFT.query.filter_by(asset_id=asset_id).first()
    return jsonify(retrieved_element.to_dict()) if retrieved_element else "NFT Not found"


@app.errorhandler(500)
def server_error():
    return "A server error: contact administrator"


@app.errorhandler(404)
def page_not_found(e):
    return "Notification: The page was not found"
