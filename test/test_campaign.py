import sys
import mox
import json
import unittest

sys.path.append("..")
from taguchi.campaign import Campaign

class TestCampaign(mox.MoxTestBase):

    def setUp(self):
        mox.MoxTestBase.setUp(self)
        self.record = Campaign(None) 
        self.record.backing = {"id": 1, "status": ""}

    def tearDown(self):
        self.record = None
        mox.MoxTestBase.tearDown(self)

    def test_record_id(self):
        self.assertEqual("1", self.record.record_id)

    def test_ref(self):
        self.record.ref = "x"
        self.assertEqual("x", self.record.ref)

    def test_name(self):
        self.record.name = "x"
        self.assertEqual("x", self.record.name)

    def test_start_datetime(self):
        self.record.start_datetime = "x"
        self.assertEqual("x", self.record.start_datetime)

    def test_xml_data(self):
        self.record.xml_data = "x"
        self.assertEqual("x", self.record.xml_data)

    def test_status(self):
        self.assertEqual("", self.record.status)

    def test_static_get(self):
        context = self.mox.CreateMockAnything()
        context.make_request("campaign", "GET", record_id=1, 
            parameters={"sort": "id", "order": "asc"}).AndReturn(
            json.dumps([{"id": 1}]))
        self.mox.ReplayAll()

        record = Campaign.get(context, 1, {"sort": "id", "order": "asc"})
        self.assertTrue(isinstance(record, Campaign))
        self.assertEqual({"id": 1}, record.backing)
        self.mox.VerifyAll()

    def test_static_find(self):
        context = self.mox.CreateMockAnything()
        context.make_request("campaign", "GET", 
            parameters={"sort": "id", "order": "asc", "offset": "1", "limit": "100"},
            query=["id-gt-1", "id-lt-100"]).AndReturn(json.dumps([{"id": 1}, {"id": 2}]))
        self.mox.ReplayAll()

        records = Campaign.find(context, "id", "asc", 1, 100, ["id-gt-1", "id-lt-100"])
        self.assertEqual(2, len(records))
        self.mox.VerifyAll()

if __name__ == "__main__":
    unittest.main()
