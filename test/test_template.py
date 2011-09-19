import sys
import mox
import json
import unittest

sys.path.append("..")
from taguchi.template import Template
from taguchi.template import TemplateRevision

class TestTemplateRevision(unittest.TestCase):

    def setUp(self):
        self.record = TemplateRevision(None, 
            {"content": "x", "format": "y", "id": 1})

    def tearDown(self):
        self.record = None

    def test_format(self):
        self.assertEqual("y", self.record.format)
        self.record.format = "new_y"
        self.assertEqual("new_y", self.record.format)

    def test_content(self):
        self.assertEqual("x", self.record.content)
        self.record.content = "new_x"
        self.assertEqual("new_x", self.record.content)

    def test_record_id(self):
        self.assertEqual("1", self.record.record_id)

class TestTemplate(mox.MoxTestBase):

    def setUp(self):
        mox.MoxTestBase.setUp(self)
        self.record = Template(None) 
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

    def test_xml_data(self):
        self.record.xml_data = "x"
        self.assertEqual("x", self.record.xml_data)

    def test_status(self):
        self.assertEqual("", self.record.status)

    def test_latest_revision(self):
        self.assertEqual(None, self.record.latest_revision)
        self.record.latest_revision = TemplateRevision(
            self.record, {"content": "x", "format": "y"})
        revision = self.record.latest_revision
        self.assertEqual("x", revision.content)
        self.assertEqual("y", revision.format)

    def test_update(self):
        context = self.mox.CreateMockAnything()
        context.make_request("template", "PUT", record_id=1, 
            data=json.dumps([{"id": 1, "ref": "ref", "revisions": []}])).AndReturn(
            json.dumps([{"id": 1, "ref": "ref", "revisions": []}]))
        self.mox.ReplayAll()

        record = Template(context)
        record.backing = {"id": 1, "ref": "ref", "revisions": []}
        record.update()
        self.assertEqual("1", record.record_id)
        self.assertEqual("ref", record.ref)
        self.mox.VerifyAll()

    def test_create(self):
        context = self.mox.CreateMockAnything()
        context.make_request("template", "POST",
            data=json.dumps([{"ref": "ref", "revisions": []}])).AndReturn(
            json.dumps([{"id": 1, "ref": "ref", "revisions": []}]))
        self.mox.ReplayAll()

        record = Template(context)
        record.backing = {"ref": "ref", "revisions": []}
        record.create()
        self.assertEqual("1", record.record_id)
        self.assertEqual("ref", record.ref)
        self.mox.VerifyAll()

    def test_static_get(self):
        context = self.mox.CreateMockAnything()
        context.make_request("template", "GET", record_id=1, 
            parameters={"sort": "id", "order": "asc"}).AndReturn(
            json.dumps([{"id": 1, "revisions": []}]))
        self.mox.ReplayAll()

        record = Template.get(context, 1, {"sort": "id", "order": "asc"})
        self.assertTrue(isinstance(record, Template))
        self.assertEqual({"id": 1, "revisions": []}, record.backing)
        self.mox.VerifyAll()

    def test_static_get_with_content(self):
        context = self.mox.CreateMockAnything()
        context.make_request("template", "GET", record_id=1, 
            parameters={"revision": "latest"}).AndReturn(
            json.dumps([{"id": 1, "revisions": []}]))
        self.mox.ReplayAll()

        record = Template.get_with_content(context, 1)
        self.assertTrue(isinstance(record, Template))
        self.assertEqual({"id": 1, "revisions": []}, record.backing)
        self.mox.VerifyAll()

    def test_static_find(self):
        context = self.mox.CreateMockAnything()
        context.make_request("template", "GET", 
            parameters={"sort": "id", "order": "asc", "offset": "1", "limit": "100"},
            query=["id-gt-1", "id-lt-100"]).AndReturn(
            json.dumps([{"id": 1, "revisions": []}, {"id": 2, "revisions": []}]))
        self.mox.ReplayAll()

        records = Template.find(context, "id", "asc", 1, 100, ["id-gt-1", "id-lt-100"])
        self.assertEqual(2, len(records))
        self.mox.VerifyAll()

if __name__ == "__main__":
    unittest.main()
