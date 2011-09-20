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
