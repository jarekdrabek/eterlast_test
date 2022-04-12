from freezegun import freeze_time

freezer = freeze_time("2022-04-11 15:30:27")
freezer.start()
from nfts import app, db
freezer.stop()

import unittest


class NftTests(unittest.TestCase):

    def setUp(self) -> None:
        db.drop_all()
        db.create_all()

    def tearDown(self) -> None:
        db.drop_all()
        db.create_all()

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
        self.assertTrue('Created NFT with asset id: ' in response.text)

    @freeze_time("2022-04-11 15:50:27")
    def test_minting_and_getting(self):
        mint_response = app.test_client().post('/nft-api/v1/mint')
        asset_id = mint_response.location.split('/')[-1]
        retrieved_element = app.test_client().get(mint_response.location)
        self.assertEquals(retrieved_element.json,
                          {'asset_id': asset_id, 'buyer': None, 'date_of_creation': '2022-04-11 15:50:27',
                           'description': None, 'external_link': None, 'name': 'name_to_change', 'picture': None,
                           'royalties': None, 'supply': None})

    def test_minting_and_getting_all_orderer_by_date_of_creation_descending(self):
        freeze_time("2022-04-11 15:45:27").start()
        asset_id1, mint_response1 = NftTests.__mint_and_return_asset_id()
        freeze_time("2022-04-11 15:50:27").start()
        asset_id2, mint_response2 = NftTests.__mint_and_return_asset_id()
        retrieved_element = app.test_client().get('/nft-api/v1/NFT/all')
        self.assertEquals(retrieved_element.json, [
            {'asset_id': asset_id2, 'buyer': None, 'date_of_creation': '2022-04-11 15:50:27',
             'description': None, 'external_link': None, 'name': 'name_to_change', 'picture': None, 'royalties': None,
             'supply': None},
            {'asset_id': asset_id1, 'buyer': None, 'date_of_creation': '2022-04-11 15:45:27',
             'description': None, 'external_link': None, 'name': 'name_to_change', 'picture': None, 'royalties': None,
             'supply': None}])

    def test_404(self):
        response = app.test_client().get('/notexisting')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.text, 'Notification: The page was not found')

    @staticmethod
    def __mint_and_return_asset_id():
        mint_response = app.test_client().post('/nft-api/v1/mint')
        asset_id = mint_response.location.split('/')[-1]
        return asset_id, mint_response



