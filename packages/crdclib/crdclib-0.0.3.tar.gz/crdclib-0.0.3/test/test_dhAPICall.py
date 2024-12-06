import unittest
import crdclib
import dhqueries


class TestDHAPICalls(unittest.TestCase):


    def test_dhAPICall(self):
        creds = crdclib.dhAPICreds('stage')
        result = crdclib.dhApiQuery(creds['url'], creds['token'], dhqueries.org_query)
        self.assertEqual(list(result.keys()), ['data'])
        self.assertIn('listApprovedStudiesOfMyOrganization', result['data'])


if __name__ == "__main__":
    unittest.main(verbosity=2)
