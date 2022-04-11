import unittest

from nfts import app


class NftTests(unittest.TestCase):

    def test_first(self):
        response = app.test_client().get('/notexisting')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.text, 'Notification: The page was not found')
