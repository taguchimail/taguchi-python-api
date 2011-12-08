import sys
import mox
import json
import unittest

sys.path.append("..")
from taguchi.record import Record
from taguchi.context import Context

class TestRecord(mox.MoxTestBase):
  
    """ 
    def test_static_get(self):
        context = self.mox.CreateMockAnything()
        context.make_request("activity", "GET", record_id=1, 
            parameters={"sort": "id", "order": "asc"}).AndReturn(json.dumps([{"id": 1}]))
        self.mox.ReplayAll()

        record = Record.get("activity", context, 1, {"sort": "id", "order": "asc"})
        self.assertTrue(isinstance(record, Record))
        self.assertEqual({"id": 1}, record.backing)
        self.mox.VerifyAll()

    def test_static_find(self):
        context = self.mox.CreateMockAnything()
        context.make_request("activity", "GET", 
            parameters={"sort": "id", "order": "asc", "offset": "1", "limit": "100"},
            query=["id-gt-1", "id-lt-100"]).AndReturn(json.dumps([{"id": 1}, {"id": 2}]))
        self.mox.ReplayAll()

        records = Record.find("activity", context, "id", "asc", 1, 100, ["id-gt-1", "id-lt-100"])
        self.assertEqual(2, len(records))
        self.mox.VerifyAll()
    """

    def test_update(self):
        context = self.mox.CreateMockAnything()
        context.make_request("activity", "PUT", record_id=10, 
            data=json.dumps([{"id": 10}])).AndReturn(json.dumps([{"id": 10, "x": 1}]))
        self.mox.ReplayAll()

        record = Record(context, resource_type="activity", backing={"id": 10})
        record.update()
        self.assertEqual({"id": 10, "x": 1}, record.backing)
        self.mox.VerifyAll()

    def test_create(self):
        context = self.mox.CreateMockAnything()
        context.make_request("activity", "POST",
            data=json.dumps([{"id": 10}])).AndReturn(json.dumps([{"id": 10, "x": 1}]))
        self.mox.ReplayAll()

        record = Record(context, resource_type="activity", backing={"id": 10})
        record.create()
        self.assertEqual({"id": 10, "x": 1}, record.backing)
        self.mox.VerifyAll()

if __name__ == "__main__":
    unittest.main()
