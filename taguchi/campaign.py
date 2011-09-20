import json

from taguchi.record import Record

class Campaign(Record):

    def __init__(self, context):
        """
        Instantiates an empty Campaign object.

        context: Context
            Determines the TM instance and organization to which the
            campaign belongs.
        """
        super(Campaign, self).__init__(context, resource_type="campaign")

    @property
    def record_id(self):
        """
        ID of the TaguchiMail campaign record.
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
        Campaign name.
        """
        return str(self.backing["name"])

    @name.setter
    def name(self, value):
        self.backing["name"] = value

    @property
    def start_datetime(self):
        """
        Date/time at which this campaign started (or is scheduled to start).
        """
        return str(self.backing["date"])

    @start_datetime.setter
    def start_datetime(self, value):
        self.backing["date"] = value

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
        Campaign status; leave None if not used.
        """
        return str(self.backing["status"])

    @staticmethod
    def get(context, record_id, parameters):
        """
        Retrieves a single Campaign based on its TaguchiMail identifier.

        context: Context
            Determines the TM instance and organization to query.
        record_id: str/int
            Contains the list's unique TaguchiMail identifier.
        """
        results = json.loads(context.make_request("campaign", "GET",
            record_id=record_id, parameters=parameters))
        record = Campaign(context)
        record.backing = results[0]
        return record

    @staticmethod
    def find(context, sort, order, offset, limit, query):
        """
        Retrieves a list of Campaign(s) based on a query.

        context: Context
            Determines the TM instance and organization to query.
        sort: str
            Indicates which of the record's fields should be used to sort
            the output.
        order: str
            Contains either 'asc' or 'desc', indicating whether the result
            list should be returned in ascending or descending order.
        offset: str/int
            Indicates the index of the first record to be returned in the
            list.
        limit: str/int
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
            * lte: mapped to SQL '<=', test if [field] is less than or
              equal to [value];
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
        results = json.loads(context.make_request("campaign", "GET",
            parameters=parameters, query=query))
        records = []
        for result in results:
            record = Campaign(context)
            record.backing = result
            records.append(record)
        return records
