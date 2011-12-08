import json

from taguchi.record import Record

class TemplateRevision(object):

    def __init__(self, template, revision=None):
        """
        Creates a new template revision, given a parent Template.
        """
        self.template = template # may be used in the future
        self.backing = revision or dict()

    @property
    def format(self):
        """
        Contains the revision's Data Description, which controls the form
        interface created by TaguchiMail to edit activities using this
        template. This document indirectly determines the structure of the
        source document used by the template's stylesheet.
        """
        return str(self.backing["format"])

    @format.setter
    def format(self, value):
        self.backing["format"] = value

    @property
    def content(self):
        """
        Contains the revision XSLT stylesheet. This is normally created within
        the TaguchiMail UI, and is designed to work with the XML documents
        created by the activity edit interface; these are created based on the
        format field, which defines allowable data types and document
        structure.
        """
        return str(self.backing["content"])

    @content.setter
    def content(self, value):
        self.backing["content"] = value

    @property
    def record_id(self):
        """
        ID of the template revision record in the database.
        """
        return str(self.backing["id"])

class Template(Record):

    def __init__(self, context):
        super(Template, self).__init__(context, resource_type="template")
        self.existing_revisions = []

    @property
    def record_id(self):
        """
        ID of the TaguchiMail template record.
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
        Template name.
        """
        return str(self.backing["name"])

    @name.setter
    def name(self, value):
        self.backing["name"] = value

    @property
    def type(self):
        """
        This is matched up with Activity types to determine what to show the
        user in the Suggested Templates/Other Templates sections.
        """
        return str(self.backing["type"])

    @type.setter
    def type(self, value):
        self.backing["type"] = value

    @property
    def subtype(self):
        """
        This can be any application-defined value.
        """
        return str(self.backing["subtype"])

    @subtype.setter
    def subtype(self, value):
        self.backing["subtype"] = value

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
        Template status; leave None if not used.
        """
        return str(self.backing["status"])

    @property
    def latest_revision(self):
        """
        Latest template revision content. If set, a new revision will be
        created upon template create/update.
        """
        if len(self.backing["revisions"]) > 0:
            return TemplateRevision(self, revision=self.backing["revisions"][0])
        elif len(self.existing_revisions) > 0:
            return TemplateRevision(self, revision=self.existing_revisions[0])
        else:
            return None

    @latest_revision.setter
    def latest_revision(self, value):
        revision = dict(content=value.content, format=value.format)
        if len(self.backing["revisions"]) > 0:
            self.backing["revisions"][0] = revision
        else:
            self.backing["revisions"].append(revision)

    def update(self):
        """
        Saves this template to the TaguchiMail database.
        """
        super(Template, self).update()
        # Need to move the existing revisions to avoid re-creating the same
        # ones if this object is saved again.
        self.existing_revisions = self.backing["revisions"]
        self.backing["revisions"] = []

    def create(self):
        """
        Creates this template in the TaguchiMail database.
        """
        super(Template, self).create()
        # Need to move the existing revisions to avoid re-creating the same
        # ones if this object is saved again.
        self.existing_revisions = self.backing["revisions"]
        self.backing["revisions"] = []

    @staticmethod
    def get(context, record_id, parameters):
        """
        Retrieves a single Template based on its TaguchiMail identifier.

        context: Context
            Determines the TM instance and organization to query.
        record_id: str/int
            Contains the list's unique TaguchiMail identifier.
        """
        results = json.loads(context.make_request("template", "GET",
            record_id=record_id, parameters=parameters))
        record = Template(context)
        record.backing = results[0]
        record.existing_revisions = record.backing["revisions"]
        # Clear out existing revisions so they're not sent back to the server
        # on update.
        record.backing["revisions"] = []
        return record

    @staticmethod
    def get_with_content(context, record_id):
        """
        Retrieve a single Template based on its TaguchiMail identifier, with
        its latest revision content.

        context: Context
            Determines the TM instance and organization to query.
        record_id: str/int
            Contains the list's unique TaguchiMail identifier.
        """
        return Template.get(context, record_id, dict(revision="latest"))

    @staticmethod
    def find(context, sort, order, offset, limit, query):
        """
        Retrieves a list of Template(s) based on a query.

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
        results = json.loads(context.make_request("template", "GET",
            parameters=parameters, query=query))
        records = []
        for result in results:
            record = Template(context)
            record.backing = result
            record.existing_revisions = record.backing["revisions"]
            # Clear out existing revisions so they're not sent back to the
            # server on update.
            record.backing["revisions"] = []
            records.append(record)
        return records
