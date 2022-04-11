from nfts.model import User, NFT, Collection, db


def init_db():
    db.drop_all()
    db.create_all()
    user1 = User(address="0x783464387jkhkjdsfs")
    col1 = Collection(name='collection1', creator=user1.address)
    col2 = Collection(name='collection2', creator=user1.address)
    db.session.add(user1)
    db.session.add(col1)
    db.session.add(col2)
    db.session.commit()
    col1 = Collection.query.first()
    nft1 = NFT(asset_id='0x390sdad0udotit', name="name1", collection_id = col1.id)
    nft2 = NFT(asset_id='0x3234sda0uasdit', name="name2", collection_id = col1.id)
    nft3 = NFT(asset_id='0x39asdgf0udotit', name="name3", collection_id = col1.id)
    nft4 = NFT(asset_id='0xasdfgsf0udotit', name="name4", collection_id = col2.id)
    nft5 = NFT(asset_id='0xlsdkfgjfdlktit', name="name5", collection_id = col2.id)
    db.session.add(nft1)
    db.session.add(nft2)
    db.session.add(nft3)
    db.session.add(nft4)
    db.session.add(nft5)
    db.session.commit()

if __name__ == '__main__':
    init_db()




