import sys
import mox
import json
import unittest

sys.path.append("..")
from taguchi.activity import Activity
from taguchi.activity import ActivityRevision

class TestActivityRevision(unittest.TestCase):

    def setUp(self):
        self.record = ActivityRevision(None, 
            {"content": "x", "approval_status": "y", "id": 1})

    def tearDown(self):
        self.record = None

    def test_content(self):
        self.assertEqual("x", self.record.content)
        self.record.content = "new_x"
        self.assertEqual("new_x", self.record.content)

    def test_approval_status(self):
        self.assertEqual("y", self.record.approval_status)
        self.record.approval_status = "new_y"
        self.assertEqual("new_y", self.record.approval_status)

    def test_record_id(self):
        self.assertEqual("1", self.record.record_id)

class TestActivity(mox.MoxTestBase):

    def setUp(self):
        mox.MoxTestBase.setUp(self)
        self.record = Activity(None) 
        self.record.backing = {"id": 1, "status": "", "revisions": []}

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

    def test_type(self):
        self.record.type = "x"
        self.assertEqual("x", self.record.type)

    def test_subtype(self):
        self.record.subtype = "x"
        self.assertEqual("x", self.record.subtype)

    def test_target_lists(self):
        self.record.target_lists = "x"
        self.assertEqual("x", self.record.target_lists)

    def test_target_views(self):
        self.record.target_views = "x"
        self.assertEqual("x", self.record.target_views)

    def test_approval_status(self):
        self.record.approval_status = "x"
        self.assertEqual("x", self.record.approval_status)

    def test_deploy_datetime(self):
        self.record.deploy_datetime = "x"
        self.assertEqual("x", self.record.deploy_datetime)

    def test_template_id(self):
        self.record.template_id = 1
        self.assertEqual("1", self.record.template_id)

    def test_campaign_id(self):
        self.record.campaign_id = 1
        self.assertEqual("1", self.record.campaign_id)

    def test_throttle(self):
        self.record.throttle = 1
        self.assertEqual(1, self.record.throttle)

    def test_xml_data(self):
        self.record.xml_data = "x"
        self.assertEqual("x", self.record.xml_data)

    def test_status(self):
        self.assertEqual("", self.record.status)

    def test_latest_revision(self):
        self.assertEqual(None, self.record.latest_revision)
        self.record.latest_revision = ActivityRevision(
            self.record, {"content": "x"})
        revision = self.record.latest_revision
        self.assertEqual("x", revision.content)

    def test_update(self):
        context = self.mox.CreateMockAnything()
        context.make_request("activity", "PUT", record_id=1, 
            data=json.dumps([{"id": 1, "ref": "ref", "revisions": []}])).AndReturn(
            json.dumps([{"id": 1, "ref": "ref", "revisions": []}]))
        self.mox.ReplayAll()

        record = Activity(context)
        record.backing = {"id": 1, "ref": "ref", "revisions": []}
        record.update()
        self.assertEqual("1", record.record_id)
        self.assertEqual("ref", record.ref)
        self.mox.VerifyAll()

    def test_create(self):
        context = self.mox.CreateMockAnything()
        context.make_request("activity", "POST",
            data=json.dumps([{"ref": "ref", "revisions": []}])).AndReturn(
            json.dumps([{"id": 1, "ref": "ref", "revisions": []}]))
        self.mox.ReplayAll()

        record = Activity(context)
        record.backing = {"ref": "ref", "revisions": []}
        record.create()
        self.assertEqual("1", record.record_id)
        self.assertEqual("ref", record.ref)
        self.mox.VerifyAll()

    def test_proof(self):
        context = self.mox.CreateMockAnything()
        context.make_request("activity", "PROOF", record_id="1",
            data=json.dumps([{"id": "1", "list_id": "1", "tag": "subject", 
            "message": "hello"}]))
        self.mox.ReplayAll()

        record = Activity(context)
        record.backing = {"id": 1}
        record.proof("1", "subject", "hello")
        self.mox.VerifyAll()

    def test_request_approval(self):
        context = self.mox.CreateMockAnything()
        context.make_request("activity", "APPROVAL", record_id="1",
            data=json.dumps([{"id": "1", "list_id": "1", "tag": "subject", 
            "message": "hello"}]))
        self.mox.ReplayAll()

        record = Activity(context)
        record.backing = {"id": 1}
        record.request_approval("1", "subject", "hello")
        self.mox.VerifyAll()

    def test_trigger(self):
        context = self.mox.CreateMockAnything()
        context.make_request("activity", "TRIGGER", record_id="1",
            data=json.dumps([{"id": "1", "test": 0, 
            "request_content": "content", "conditions": ["1"]}]))
        self.mox.ReplayAll()

        record = Activity(context)
        record.backing = {"id": 1}
        record.trigger(["1"], "content", False)
        self.mox.VerifyAll()

    def test_static_get(self):
        context = self.mox.CreateMockAnything()
        context.make_request("activity", "GET", record_id=1, 
            parameters={"sort": "id", "order": "asc"}).AndReturn(
            json.dumps([{"id": 1, "revisions": []}]))
        self.mox.ReplayAll()

        record = Activity.get(context, 1, {"sort": "id", "order": "asc"})
        self.assertTrue(isinstance(record, Activity))
        self.assertEqual({"id": 1, "revisions": []}, record.backing)
        self.mox.VerifyAll()

    def test_static_get_with_content(self):
        context = self.mox.CreateMockAnything()
        context.make_request("activity", "GET", record_id=1, 
            parameters={"revision": "latest"}).AndReturn(
            json.dumps([{"id": 1, "revisions": []}]))
        self.mox.ReplayAll()

        record = Activity.get_with_content(context, 1)
        self.assertTrue(isinstance(record, Activity))
        self.assertEqual({"id": 1, "revisions": []}, record.backing)
        self.mox.VerifyAll()

    def test_static_find(self):
        context = self.mox.CreateMockAnything()
        context.make_request("activity", "GET", 
            parameters={"sort": "id", "order": "asc", "offset": "1", "limit": "100"},
            query=["id-gt-1", "id-lt-100"]).AndReturn(
            json.dumps([{"id": 1, "revisions": []}, {"id": 2, "revisions": []}]))
        self.mox.ReplayAll()

        records = Activity.find(context, "id", "asc", 1, 100, ["id-gt-1", "id-lt-100"])
        self.assertEqual(2, len(records))
        self.mox.VerifyAll()

if __name__ == "__main__":
    unittest.main()
