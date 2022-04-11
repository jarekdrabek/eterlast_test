from datetime import datetime

from flask import Flask

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)




@app.route('/nft-api/v1/mint', methods=['POST'])
def mint():
    pass


@app.route('/nft-api/v1/NFT/<string:id>', methods=['GET'])
def get_nft(id):
    return f"{id}"


@app.route('/nft-api/v1/NFT/all', methods=['GET'])
def get_all_nft():
    pass


if __name__ == '__main__':
    app.run(debug=True)