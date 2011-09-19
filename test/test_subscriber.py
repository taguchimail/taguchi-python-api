import sys
import mox
import json
import unittest

sys.path.append("..")
from taguchi.subscriber import Subscriber
from taguchi.subscriber import SubscriberList

class TestSubscriber(mox.MoxTestBase):

    def setUp(self):
        mox.MoxTestBase.setUp(self)
        self.record = Subscriber(None) 
        self.record.backing = {"id": 1, "social_rating": 2, "social_profile": 3, 
            "custom_fields": [{"field": "x", "data": "x"}], 
            "lists": [{"list_id": 1, "unsubscribed": None, "option": "option"},
                      {"list_id": 3, "unsubscribed": "u", "option": "option"}]}

    def tearDown(self):
        self.record = None
        mox.MoxTestBase.tearDown(self)

    def test_record_id(self):
        self.assertEqual("1", self.record.record_id)

    def test_ref(self):
        self.record.ref = "x"
        self.assertEqual("x", self.record.ref)

    def test_title(self):
        self.record.title = "x"
        self.assertEqual("x", self.record.title)

    def test_firstname(self):
        self.record.firstname = "x"
        self.assertEqual("x", self.record.firstname)

    def test_lastname(self):
        self.record.lastname = "x"
        self.assertEqual("x", self.record.lastname)

    def test_notifications(self):
        self.record.notifications = "x"
        self.assertEqual("x", self.record.notifications)

    def test_extra(self):
        self.record.extra = "x"
        self.assertEqual("x", self.record.extra)

    def test_phone(self):
        self.record.phone = "x"
        self.assertEqual("x", self.record.phone)

    def test_dob(self):
        self.record.dob = "x"
        self.assertEqual("x", self.record.dob)

    def test_address(self):
        self.record.address = "x"
        self.assertEqual("x", self.record.address)

    def test_address2(self):
        self.record.address2 = "x"
        self.assertEqual("x", self.record.address2)

    def test_address3(self):
        self.record.address3 = "x"
        self.assertEqual("x", self.record.address3)

    def test_suburb(self):
        self.record.suburb = "x"
        self.assertEqual("x", self.record.suburb)

    def test_state(self):
        self.record.state = "x"
        self.assertEqual("x", self.record.state)

    def test_country(self):
        self.record.country = "x"
        self.assertEqual("x", self.record.country)

    def test_postcode(self):
        self.record.postcode = "x"
        self.assertEqual("x", self.record.postcode)

    def test_gender(self):
        self.record.gender = "x"
        self.assertEqual("x", self.record.gender)

    def test_email(self):
        self.record.email = "x"
        self.assertEqual("x", self.record.email)

    def test_social_rating(self):
        self.assertEqual("2", self.record.social_rating)

    def test_social_profile(self):
        self.assertEqual("3", self.record.social_profile)

    def test_unsubscribe_datetime(self):
        self.record.unsubscribe_datetime = "x"
        self.assertEqual("x", self.record.unsubscribe_datetime)

    def test_bounce_datetime(self):
        self.record.bounce_datetime = "x"
        self.assertEqual("x", self.record.bounce_datetime)

    def test_xml_data(self):
        self.record.xml_data = "x"
        self.assertEqual("x", self.record.xml_data)

    def test_get_custom_field(self):
        self.assertEqual("x", self.record.get_custom_field("x"))
        self.assertEqual(None, self.record.get_custom_field("y"))

    def test_set_custom_field(self):
        self.record.set_custom_field("x", "y")
        self.assertEqual("y", self.record.get_custom_field("x"))

    def test_is_subscribed_to_list(self):
        self.assertTrue(self.record.is_subscribed_to_list("1"))
        self.assertFalse(self.record.is_subscribed_to_list("2"))

    def test_get_subscription_option(self):
        self.assertEqual("option", self.record.get_subscription_option("1"))
        self.assertEqual(None, self.record.get_subscription_option("2"))

    def test_is_subscribed_from_list(self):
        self.assertFalse(self.record.is_unsubscribed_from_list("1"))
        self.assertTrue(self.record.is_unsubscribed_from_list("3"))

    def test_get_subscribed_list_ids(self):
        self.assertEqual(["1"], self.record.get_subscribed_list_ids())
 
    def test_get_subscribed_lists(self):
        self.mox.StubOutWithMock(SubscriberList, "get")
        SubscriberList.get(None, "1", None).AndReturn(SubscriberList(None))
        self.mox.ReplayAll()

        lists = self.record.get_subscribed_lists()
        self.assertEqual(1, len(lists))
        self.assertTrue(isinstance(lists[0], SubscriberList))
        self.mox.VerifyAll()

    def test_get_unsubscribed_list_ids(self):
        self.assertEqual(["3"], self.record.get_unsubscribed_list_ids())
 
    def test_get_unsubscribed_lists(self):
        self.mox.StubOutWithMock(SubscriberList, "get")
        SubscriberList.get(None, "3", None).AndReturn(SubscriberList(None))
        self.mox.ReplayAll()

        lists = self.record.get_unsubscribed_lists()
        self.assertEqual(1, len(lists))
        self.assertTrue(isinstance(lists[0], SubscriberList))
        self.mox.VerifyAll()

    def test_subscribe_to_list(self):
        self.assertFalse(self.record.is_subscribed_to_list("2"))
        self.record.subscribe_to_list("2", "option")
        self.assertTrue(self.record.is_subscribed_to_list("2"))
        
    def test_unsubscribe_from_list(self):
        self.assertFalse(self.record.is_unsubscribed_from_list("1"))
        self.record.unsubscribe_from_list("1")
        self.assertTrue(self.record.is_unsubscribed_from_list("1"))

    def test_create_or_update(self):
        context = self.mox.CreateMockAnything()
        context.make_request("subscriber", "CREATEORUPDATE",
            data=json.dumps([{"id": 1, "ref": "ref"}])).AndReturn(
            json.dumps([{"id": 1, "ref": "ref"}]))
        self.mox.ReplayAll()

        record = Subscriber(context)
        record.backing = {"id": 1, "ref": "ref"}
        record.create_or_update()
        self.assertEqual("1", record.record_id)
        self.assertEqual("ref", record.ref)
        self.mox.VerifyAll()

    def test_static_get(self):
        context = self.mox.CreateMockAnything()
        context.make_request("subscriber", "GET", record_id=1, 
            parameters={"sort": "id", "order": "asc"}).AndReturn(
            json.dumps([{"id": 1}]))
        self.mox.ReplayAll()

        record = Subscriber.get(context, 1, {"sort": "id", "order": "asc"})
        self.assertTrue(isinstance(record, Subscriber))
        self.assertEqual({"id": 1}, record.backing)
        self.mox.VerifyAll()

    def test_static_find(self):
        context = self.mox.CreateMockAnything()
        context.make_request("subscriber", "GET", 
            parameters={"sort": "id", "order": "asc", "offset": "1", "limit": "100"},
            query=["id-gt-1", "id-lt-100"]).AndReturn(
            json.dumps([{"id": 1}, {"id": 2}]))
        self.mox.ReplayAll()

        records = Subscriber.find(context, "id", "asc", 1, 100, ["id-gt-1", "id-lt-100"])
        self.assertEqual(2, len(records))
        self.mox.VerifyAll()

class TestSubscriberList(mox.MoxTestBase):

    def setUp(self):
        mox.MoxTestBase.setUp(self)
        self.record = SubscriberList(None)
        self.record.backing = {"id": 1, "timestamp": "x", "status": ""}

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

    def test_creation_datetime(self):
        self.assertEqual("x", self.record.creation_datetime)

    def test_xml_data(self):
        self.record.xml_data = "x"
        self.assertEqual("x", self.record.xml_data)

    def test_status(self):
        self.assertEqual("", self.record.status)

    def test_subscribe_subscriber(self):
        subscriber = self.mox.CreateMockAnything()
        subscriber.subscribe_to_list(self.record, "option")
        self.mox.ReplayAll()

        self.record.subscribe_subscriber(subscriber, "option")
        self.mox.VerifyAll()

    def test_unsubscribe_unsubscriber(self):
        subscriber = self.mox.CreateMockAnything()
        subscriber.unsubscribe_from_list(self.record)
        self.mox.ReplayAll()

        self.record.unsubscribe_subscriber(subscriber)
        self.mox.VerifyAll()

    def test_get_subscribers(self):
        self.mox.StubOutWithMock(Subscriber, "find", True)
        Subscriber.find(None, "id", "asc", 0, 100, ["list_id-eq-1"])
        self.mox.ReplayAll()

        self.record.get_subscribers(0, 100)
        self.mox.VerifyAll()

    def test_static_get(self):
        context = self.mox.CreateMockAnything()
        context.make_request("list", "GET", record_id=1,
            parameters={"sort": "id", "order": "asc"}).AndReturn(
            json.dumps([{"id": 1}]))
        self.mox.ReplayAll()

        record = SubscriberList.get(context, 1, {"sort": "id", "order": "asc"})
        self.assertTrue(isinstance(record, SubscriberList))
        self.assertEqual({"id": 1}, record.backing)
        self.mox.VerifyAll()

    def test_static_find(self):
        context = self.mox.CreateMockAnything()
        context.make_request("list", "GET",
            parameters={"sort": "id", "order": "asc", "offset": "1", "limit": "100"},
            query=["id-gt-1", "id-lt-100"]).AndReturn(json.dumps([{"id": 1}, {"id": 2}]))
        self.mox.ReplayAll()

        records = SubscriberList.find(context, "id", "asc", 1, 100, ["id-gt-1", "id-lt-100"])
        self.assertEqual(2, len(records))
        self.mox.VerifyAll()

if __name__ == "__main__":
    unittest.main()
