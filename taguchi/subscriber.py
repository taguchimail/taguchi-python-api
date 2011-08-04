import json
import urllib
import httplib

from taguchi.context import Context
from taguchi.record import Record

class Subscriber(Record):

    def __init__(self, context):
        """
        Instantiates an empty Subscriber object.

        context: Context
            Determines the TM instance and organization to which the
            subscriber belongs.
        """
        super(Subscriber, self).__init__(context)
        self.resource_type = "subscriber"

    @property
    def record_id(self):
        """
        ID of the TaguchiMail subscriber record.
        """
        return str(self.backing["id"])

    @property
    def ref(self):
        """
        External ID/reference, intended to store external application primary
        keys. If not None, the field must be unique.
        """
        return str(self.backing["ref"])

    @ref.setter
    def ref(self, value):
        self.backing["ref"] = value

    @property
    def title(self):
        """
        Title (Mr, Mrs etc).
        """
        return str(self.backing["title"])

    @title.setter
    def title(self, value):
        self.backing["title"] = value

    @property
    def firstname(self):
        """
        First (given) name.
        """
        return str(self.backing["firstname"])

    @firstname.setter
    def firstname(self, value):
        self.backing["firstname"] = value

    @property
    def lastname(self):
        """
        Last (family) name.
        """
        return str(self.backing["lastname"])

    @lastname.setter
    def lastname(self, value):
        self.backing["lastname"] = value

    @property
    def notifications(self):
        """
        Notifications field, can store arbitrary application data.
        """
        return str(self.backing["notifications"])

    @notifications.setter
    def notifications(self, value):
        self.backing["notifications"] = value

    @property
    def extra(self):
        """
        Extra field, can store arbitrary application data.
        """
        return str(self.backing["extra"])

    @extra.setter
    def extra(self, value):
        self.backing["extra"] = value

    @property
    def phone(self):
        """
        Phone number.
        """
        return str(self.backing["phone"])

    @extra.setter
    def phone(self, value):
        self.backing["phone"] = value

    @property
    def dob(self):
        """
        Date of birth.
        """
        return str(self.backing["dob"])

    @dob.setter
    def dob(self, value):
        self.backing["dob"] = value

    @property
    def address(self):
        """
        Postal address line 1.
        """
        return str(self.backing["address"])

    @address.setter
    def address(self, value):
        self.backing["address"] = value

    @property
    def address2(self):
        """
        Postal address line 2.
        """
        return str(self.backing["address2"])

    @address2.setter
    def address2(self, value):
        self.backing["address2"] = value

    @property
    def address3(self):
        """
        Postal address line 3.
        """
        return str(self.backing["address3"])

    @address3.setter
    def address3(self, value):
        self.backing["address3"] = value

    @property
    def suburb(self):
        """
        Postal address city, suburb or locality.
        """
        return str(self.backing["suburb"])

    @suburb.setter
    def suburb(self, value):
        self.backing["suburb"] = value

    @property
    def state(self):
        """
        Postal address state or region.
        """
        return str(self.backing["state"])

    @state.setter
    def state(self, value):
        self.backing["state"] = value

    @property
    def country(self):
        """
        Postal address country.
        """
        return str(self.backing["country"])

    @country.setter
    def country(self, value):
        self.backing["country"] = value

    @property
    def postcode(self):
        """
        Postal code.
        """
        return str(self.backing["postcode"])

    @postcode.setter
    def postcode(self, value):
        self.backing["postcode"] = value

    @property
    def gender(self):
        """
        Gender (M/F, male/female).
        """
        return str(self.backing["gender"])

    @gender.setter
    def gender(self, value):
        self.backing["gender"] = value

    @property
    def email(self):
        """
        Email address. If external ID is None, this must be unique.
        """
        return str(self.backing["email"])

    @email.setter
    def email(self, value):
        self.backing["email"] = value

    @property
    def social_rating(self):
        """
        Social media influence rating. Ordinal positive integer scale; higher
        values mean more public profile data, more status updates, and/or more
        friends. Read-only as this is calculated by TaguchiMail's social media
        subsystem.
        """
        return str(self.backing["social_rating"])

    @property
    def social_profile(self):
        """
        Social media aggregate profile. JSON data structure similar to the
        OpenSocial v1.1 Person schema.
        """
        return str(self.backing["social_profile"])

    @property
    def unsubscribe_datetime(self):
        """
        Date/time at which this subscriber globally unsubscribed (or None).
        """
        return str(self.backing["unsubscribed"])

    @unsubscribe_datetime.setter
    def unsubscribe_datetime(self, value):
        self.backing["unsubscribed"] = value

    @property
    def bounce_datetime(self):
        """
        Date/time at which this subscriber's email address was marked as
        invalid (or None).
        """
        return str(self.backing["bounced"])

    @bounce_datetime.setter
    def bounce_datetime(self, value):
        self.backing["bounced"] = value

    @property
    def xml_data(self):
        """
        Arbitrary application XML data store.
        """
        return str(self.backing["data"])

    @xml_data.setter
    def xml_data(self, value):
        self.backing["data"] = value

    def get_custom_field(self, field):
        """
        Retrieves a custom field value by field name.

        field: str
            Indicates the custom field to retrieve.
        """
        self.backing["custom_fields"] = self.backing.get("custom_fields", []) or []
        for field_data in self.backing["custom_fields"]:
            if str(field_data["field"]) == field:
                return str(field_data["data"])
        return None

    def set_custom_field(self, field, data):
        """
        Sets a custom field value by field.

        field: str
            Contains the name of the field to set. If a field with that name
            is already defined for this subscriber, the new value will
            overwrite the old one.
        data: str
            Contains the field's data. If a field is intended to store array
            or other complex data types, this should be JSON-encoded (or
            serialized to XML depending on application preference).
        """
        self.backing["custom_fields"] = self.backing.get("custom_fields", []) or []
        for i in range(len(self.backing["custom_fields"])):
            if str(self.backing["custom_fields"][i]["field"]) == field:
                self.backing["custom_fields"][i]["data"] = data
                return
        # Field was not found in the array, so add it.
        cf = dict(field=field, data=data)
        self.backing["custom_fields"].append(cf)

    def is_subscribed_to_list(self, list):
        """
        Checks the subscription status of a specific list.

        list: str/SubscriberList
            Contains the list ID/list to check subscription status for.
        """
        if isinstance(list, str):
            self.backing["lists"] = self.backing.get("lists", []) or []
            for list in self.backing["lists"]:
                if str(list["list_id"]) == list:
                    if str(list["unsubscribed"]) is None:
                        return True
                    else:
                        return False
            return False
        else:
            return self.is_subscribed_to_list(list.record_id)

    def get_subscription_option(self, list):
        """
        Retrieves teh subscription option (arbitrary application data) for a
        specific list.

        list: str/SubscriberList
            Contains the list ID/list to retrieve subscription option for.
        """
        if isinstance(list, str):
            self.backing["lists"] = self.backing.get("lists", []) or []
            for list in self.backing["lists"]:
                if str(list["list_id"]) == list:
                    return str(list["option"])
            return None
        else:
            return self.get_subscription_option(list.record_id)

    def is_unsubscribed_from_list(self, list):
        """
        Checks the unsubscription status of a specific list.

        list: str/SubscriberList
            Contains the list ID/list to check unsubscription status for.
        """
        if isinstance(list, str):
            self.backing["lists"] = self.backing.get("lists", []) or []
            for list in self.backing["lists"]:
                if str(list["list_id"]) == list:
                    if str(list["unsubscribed"]) is None:
                        return False
                    else:
                        return True
            return False
        else:
            self.is_unsubscribed_from_list(list.record_id)

    def get_subscribed_list_ids(self):
        """
        Retrieves all lists to which this record is subscribed.
        """
        self.backing["lists"] = self.backing.get("lists", []) or []
        lists = []
        for list in self.backing["lists"]:
            if list["unsubscribed"] is None:
                lists.append(str(list["list_id"]))
        return lists

    def get_subscribed_lists(self):
        list_ids = self.get_subscribed_list_ids()
        lists = []
        for list_id in list_ids:
            lists.append(SubscriberList.get(self.context, list_id, None))
        return lists

    def get_unsubscribed_list_ids(self):
        """
        Retrieves all lists from which this record is unsubscribed.
        """
        self.backing["lists"] = self.backing.get("lists", []) or []
        lists = []
        for list in self.backing["lists"]:
            if list["unsubscribed"] is not None:
                lists.append(str(list["list_id"]))
        return lists

    def get_unsubscribed_lists(self):
        list_ids = self.get_unsubscribed_list_ids()
        lists = []
        for list_id in list_ids:
            lists.append(SubscriberList.get(self.context, list_id, None))
        return lists

    def subscribe_to_list(self, list, option):
        """
        Adds the subscriber to a specific list, resetting the unsubscribe flag
        if previously set.

        list: str/SubscriberList
            Contains the list ID/list which should be added.
        option: str
            Contains the list subscription option (arbitrary application
            data).
        """
        if isinstance(list, str):
            self.backing["lists"] = self.backing.get("lists", []) or []
            for i in range(len(self.backing["lists"])):
                if str(self.backing["lists"][i]["list_id"]) == list:
                    self.backing["lists"][i]["option"] = option
                    self.backing["lists"][i]["unsubscribed"] = None
                    return
            # List was not found in the array, so add it.
            list = dict(list_id=int(list), option=option)
            self.backing["lists"].append(list)
        else:
            self.subscribe_to_list(list.record_id, option)

    def unsubscribe_from_list(self, list):
        """
        Unsubscribe from a specific list, adding the list if not already
        subscribed.

        list: str/SubscriberList
            Contains the list ID/list from which the record should be
            unsubscribed.
        """
        if isinstance(list, str):
            self.backing["lists"] = self.backing.get("lists", []) or []
            for i in range(len(self.backing["lists"])):
                if str(self.backing["lists"][i]["list_id"]) == list and \
                    self.backing["lists"][i]["unsubscribed"] is None:
                    self.backing["lists"][i]["unsubscribed"] = True
                    return
            # List was not found in the array, so add it.
            list = dict(list_id=int(list), unsubscribed=True)
            self.backing["lists"].append(list)
        else:
            self.unsubscribe_from_list(list.record_id)

    def create_or_update(self):
        """
        Creates this record in the TaguchiMail database if it doesn't already
        exist (based on a search for records with the same ref of email in
        that order). If it does, simply update what's already in the database.
        Fields not written to the backing store (via property update) will not
        be over-written in the database.
        """
        data = [self.backing]
        results = json.loads(self.context.make_request(self.resource_type,
            "CREATEORUPDATE", data=json.dumps(data)))
        self.backing = results[0]

    @staticmethod
    def get(context, record_id, parameters):
        """
        Retreives a single Subscriber based on its TaguchiMail identifier.

        context: Context
            Determines the TM instance and organization to query.
        record_id: str
            Contains the record's unique TaguchiMail identifier.
        """
        results = json.loads(context.make_request("subscriber", "GET",
            record_id, parameters=parameters))
        rec = Subscriber(context)
        rec.backing = results[0]
        return rec

    @staticmethod
    def find(context, sort, order, offset, limit, query):
        """
        Retrieves a list of Subscribers based on a query.

        context: Context
            Determines the TM instance and organization to query.
        sort: str
            Indicates which of the record's fields should be used to sort
            the output.
        order: str
            Contains either 'asc' or 'desc', indicating whether the result
            list should be returned in ascending or descending order.
        offset: str
            Indicates the index of the first record to be returned in the
            list.
        limit: str
            Indicates the maximum number of records to return.
        query: list
            Contains query predicates, each of the form: [field]-[operator]-
            [value] where [field] is one of the defined resource fields,
            [operator] is one of the below-listed comparison operators, and
            [value] is a string value to which the field should be compared.

            Supported operators:
            * eq: mapped to SQL '=', test for equality between [field] and
              [value] (case-sensitive for strings);
            * neq: mapped to SQL '!=', test for inequality between [field] and
              [value] (case-sensitive for strings);
            * lt: mapped to SQL '<', test if [field] is less than [value];
            * gt: mapped to SQL '>', test if [field] is greater than [value];
            * lte: mapped to SQL '<=', test if [field] is less than or equal
              to [value];
            * gte: mapped to SQL '>=', test if [field] is greater than or
              equal to [value];
            * re: mapped to PostgreSQL '~', interprets [value] as POSIX
              regular expression and test if [field] matches it;
            * rei: mapped to PostgreSQL '~*', performs a case-insensitive
              POSIX regular expression match;
            * like: mapped to SQL 'LIKE' (case-sensitive);
            * is: mapped to SQL 'IS', should be used to test for NULL values
              in the database as [field]-eq-null is always false;
            * nt: mapped to SQL 'IS NOT', should be used to test for NOT NULL
              values in the database as [field]-neq-null is always false.
        """
        parameters = dict(sort=sort, order=order, offset=str(offset),
            limit=str(limit))
        results = json.loads(context.make_request("subscriber", "GET",
            parameters=parameters, query=query))
        records = []
        for result in results:
            rec = Subscriber(context)
            rec.backing = result
            records.append(rec)
        return records

class SubscriberList(Record):

    def __init__(self, context):
        super(SubscriberList, self).__init__(context)
        self.resource_type = "list"

    @property
    def record_id(self):
        """
        ID of the TaguchiMail list record.
        """
        return str(self.backing["id"])

    @property
    def ref(self):
        """
        External ID/reference, intended to store external application primary
        keys. If not None, the field must be unique.
        """
        return str(self.backing["ref"])

    @ref.setter
    def ref(self, value):
        self.backing["ref"] = value

    @property
    def name(self):
        """
        List name.
        """
        return str(self.backing["name"])

    @name.setter
    def name(self, value):
        self.backing["name"] = value

    @property
    def type(self):
        """
        List type; if set to "proof", "approval" or "notification" this list
        becomes a utility list accessible only via settings; if set to another
        not-null vlaue the list is hidden from the UI buy may still be used by
        API methods; if None, the list is a public opt-in list. Leave None if
        not used.
        """
        return str(self.backing["type"])

    @type.setter
    def type(self, value):
        self.backing["type"] = value

    @property
    def creation_datetime(self):
        """
        Date/time at which this list was created.
        """
        return str(self.backing["timestamp"])

    @property
    def xml_data(self):
        """
        Arbitrary application XML data store.
        """
        return str(self.backing["data"])

    @xml_data.setter
    def xml_data(self, value):
        self.backing["data"] = value

    @property
    def status(self):
        """
        List status; leave None if not used.
        """
        return str(self.backing["status"])

    def subscribe_subscriber(self, subscriber, option):
        """
        Adds a subscriber to this list with an application-defined
        subscription option.

        subscriber: Subscriber
            A subscriber to add.
        option: str
            A subscription option.
        """
        subscriber.subscribe_to_list(self, option)

    def unsubscribe_subscriber(self, subscriber):
        """
        Unsubscribes a subscriber from this list (adding it first if
        necessary).

        subscriber: Subscriber
            A subscriber to unsubscribe.
        """
        subscriber.unsubscribe_from_list(self)

    def get_subscribers(self, offset, limit):
        """
        Retrieves (limit) subscribers to this list (regardless of
        opt-in/opt-out status), starting with the (offset)th subscriber.
        """
        return Subscriber.find(self.context, "id", "asc", offset, limit,
            ["list_id-eq-" + self.record_id])

    @staticmethod
    def get(context, record_id, parameters):
        """
        Retreives a single SubscriberList based on its TaguchiMail identifier.

        context: Context
            Determines the TM instance and organization to query.
        record_id: str
            Contains the list's unique TaguchiMail identifier.
        """
        results = json.loads(context.make_request("list", "GET",
            record_id, parameters=parameters))
        rec = SubscriberList(context)
        rec.backing = results[0]
        return rec

    @staticmethod
    def find(context, sort, order, offset, limit, query):
        """
        Retrieves a list of SubscriberLists based on a query.

        context: Context
            Determines the TM instance and organization to query.
        sort: str
            Indicates which of the record's fields should be used to sort
            the output.
        order: str
            Contains either 'asc' or 'desc', indicating whether the result
            list should be returned in ascending or descending order.
        offset: str
            Indicates the index of the first record to be returned in the
            list.
        limit: str
            Indicates the maximum number of records to return.
        query: list
            Contains query predicates, each of the form: [field]-[operator]-
            [value] where [field] is one of the defined resource fields,
            [operator] is one of the below-listed comparison operators, and
            [value] is a string value to which the field should be compared.

            Supported operators:
            * eq: mapped to SQL '=', test for equality between [field] and
              [value] (case-sensitive for strings);
            * neq: mapped to SQL '!=', test for inequality between [field] and
              [value] (case-sensitive for strings);
            * lt: mapped to SQL '<', test if [field] is less than [value];
            * gt: mapped to SQL '>', test if [field] is greater than [value];
            * lte: mapped to SQL '<=', test if [field] is less than or equal
              to [value];
            * gte: mapped to SQL '>=', test if [field] is greater than or
              equal to [value];
            * re: mapped to PostgreSQL '~', interprets [value] as POSIX
              regular expression and test if [field] matches it;
            * rei: mapped to PostgreSQL '~*', performs a case-insensitive
              POSIX regular expression match;
            * like: mapped to SQL 'LIKE' (case-sensitive);
            * is: mapped to SQL 'IS', should be used to test for NULL values
              in the database as [field]-eq-null is always false;
            * nt: mapped to SQL 'IS NOT', should be used to test for NOT NULL
              values in the database as [field]-neq-null is always false.
        """
        parameters = dict(sort=sort, order=order, offset=str(offset),
            limit=str(limit))
        results = json.loads(context.make_request("list", "GET",
            parameters=parameters, query=query))
        records = []
        for result in results:
            rec = SubscriberList(context)
            rec.backing = result
            records.append(rec)
        return records
