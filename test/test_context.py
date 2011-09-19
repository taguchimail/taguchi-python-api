import sys
import mox
import json
import httplib
import unittest

sys.path.append("..")
from taguchi.context import Context

class TestContext(mox.MoxTestBase):
   
    def setUp(self):
        mox.MoxTestBase.setUp(self)
        self.context = Context("127.0.0.1", "test@taguchimail.com", "X", 1)

    def tearDown(self):
        self.context = None
        mox.MoxTestBase.tearDown(self)

    def test_make_request_with_data(self):
        conn = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(httplib, "HTTPSConnection", True)
        httplib.HTTPSConnection("127.0.0.1", timeout=60).AndReturn(conn)
        method = "POST"
        qs = "/admin/api/1/activity/1?_method=update&auth=test%40taguchimail.com%7CX"
        data = json.dumps({"id": 1})
        headers = {'UserAgent': 'TMAPIv4 python wrapper', 'Content-Length': 9, 
            'Content-Type': 'application/json', 'Accept': 'application/json', 
            'PreAuthenticate': 'true'}
        conn.request(method, qs, data, headers)
        reply = self.mox.CreateMockAnything()
        conn.getresponse().AndReturn(reply)
        reply.read().AndReturn("200")
        conn.close()
        self.mox.ReplayAll()

        result = self.context.make_request("activity", "update", record_id=1, 
            data=json.dumps({"id": 1}))
        self.assertEqual("200", result)
        self.mox.VerifyAll()

    def test_make_request_without_data(self):
        conn = self.mox.CreateMockAnything()
        self.mox.StubOutWithMock(httplib, "HTTPSConnection", True)
        httplib.HTTPSConnection("127.0.0.1", timeout=60).AndReturn(conn)
        method = "POST"
        qs = "/admin/api/1/activity/1?_method=view&auth=test%40taguchimail.com%7CX"
        data = None
        headers = {'UserAgent': 'TMAPIv4 python wrapper', 'Accept': 'application/json', 
            'PreAuthenticate': 'true'}
        conn.request(method, qs, data, headers)
        reply = self.mox.CreateMockAnything()
        conn.getresponse().AndReturn(reply)
        reply.read().AndReturn("200")
        conn.close()
        self.mox.ReplayAll()

        result = self.context.make_request("activity", "view", record_id=1)
        self.assertEqual("200", result)
        self.mox.VerifyAll()

if __name__ == "__main__":
    unittest.main()
