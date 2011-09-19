import json

class Record(object):
    """
    Base class for TM record types.
    """

    def __init__(self, context, resource_type=None, backing=None):
        """
        Initiates an empty Record object.

        context: Context
            Determines the TM instance and organization to which the record
            belongs.
        resource_type: str
            The type of resource this record represents e.g. activity.
        backing: dict
            The data backing the record.
        """
        self.context = context
        self.resource_type = resource_type or None
        self.backing = backing or dict()

    @staticmethod
    def get(resource_type, context, record_id, parameters):
        """
        Retreives a single Record based on its TaguchiMail identifier.

        resource_type: str
            Contains the resource type (passed in by subclass methods).
        context: Context
            Determines the TM instance and organization to query.
        record_id: int
            Contains the record's unique TaguchiMail identifier.
        parameters: dict
            Contains additional parameters to the request.
        """
        results = json.loads(context.make_request(resource_type, "GET",
            record_id=record_id, parameters=parameters))
        return Record(context, backing=results[0])

    @staticmethod
    def find(resource_type, context, sort, order, offset, limit, query):
        """
        Retrieves a list of Records based on a query.

        resource_type: str
            Contains the resource type (passed in by sublass methods).
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
        results = json.loads(context.make_request(resource_type, "GET",
            parameters=parameters, query=query))
        records = []
        for result in results:
            records.append(Record(context, backing=result))
        return records

    def update(self):
        """
        Saves this record to the TaguchiMail database.
        """
        data = [self.backing]
        results = json.loads(self.context.make_request(self.resource_type,
            "PUT", record_id=self.backing["id"], data=json.dumps(data)))
        self.backing = results[0]

    def create(self):
        """
        Creates this record in the TaguchiMail database.
        """
        data = [self.backing]
        results = json.loads(self.context.make_request(self.resource_type,
            "POST", data=json.dumps(data)))
        self.backing = results[0]
