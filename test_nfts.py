import json
import unittest

from nfts import app, db


class NftTests(unittest.TestCase):

    def setUp(self) -> None:
        db.create_all()

    def tearDown(self) -> None:
        db.drop_all()

    def test_getting_not_existing_nft(self):
        response = app.test_client().get('/nft-api/v1/NFT/notexistingone')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.text, 'NFT Not found')

    def test_getting_all_nfts(self):
        response = app.test_client().get('/nft-api/v1/NFT/all')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json, [])

    def test_mint_response(self):
        response = app.test_client().post('/nft-api/v1/mint')
        self.assertEquals(response.status_code, 201)
        self.assertIsNotNone(response.location)
        self.assertTrue('Created NFT with asset id: ' in response.text )

    def test_minting_and_getting(self):
        mint_response = app.test_client().post('/nft-api/v1/mint')
        asset_id = mint_response.location.split('/')[-1]
        retrieved_element = app.test_client().get(mint_response.location)
        self.assertEquals(retrieved_element.json, {'asset_id': asset_id, 'name': 'name_to_change'})

    def test_minting_and_getting_all(self):
        asset_id1, mint_response1 = self.__mint_and_return_asset_id()
        asset_id2, mint_response2 = self.__mint_and_return_asset_id()
        retrieved_element = app.test_client().get('/nft-api/v1/NFT/all')
        self.assertEquals(retrieved_element.json, [{'asset_id': asset_id1, 'name': 'name_to_change'}, {'asset_id': asset_id2, 'name': 'name_to_change'}])

    def test_404(self):
        response = app.test_client().get('/notexisting')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.text, 'Notification: The page was not found')

    def __mint_and_return_asset_id(self):
        mint_response = app.test_client().post('/nft-api/v1/mint')
        asset_id = mint_response.location.split('/')[-1]
        return asset_id, mint_response
