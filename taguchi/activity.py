import json
import urllib
import httplib

from taguchi.context import Context
from taguchi.record import Record

class ActivityRevision(object):

    def __init__(self, activity, content=None, revision=None):
        """
        Creates a new activity revision, given a parent Activity and a content
        document (a.k.a. Source Document).
        """
        self.activity = activity
        self.backing = revision if revision else dict()
        self.content = content

    @property
    def content(self):
        """
        Contains revision XML content. This is typically set up in the
        TaguchiMail UI, and normally includes an XML document structure based
        on RSS. However, if UI access is not required, this content can have
        an arbitrary (valid) structure; the only requirement is that the
        transform associated with the template convert this content into a
        valid intermediate MIME document.
        """
        return str(self.backing["content"])

    @content.setter
    def content(self, value):
        self.backing["format"] = value

    @property
    def approval_status(self):
        """
        If 'deployed', this revision is publicly available, otherwise only
        test events may use this revision.
        """
        return str(self.backing["approval_status"])

    @approval_status.setter
    def approval_status(self, value):
        self.backing["approval_status"] = value

    @property
    def record_id(self):
        """
        ID of the activity revision record in the database.
        """
        return str(self.backing["id"])


class Activity(Record):

    def __init__(self, context):
        super(Activity, self).__init__(context)
        self.resource_type = "activity"
        self.existing_revisions = []

    @property
    def record_id(self):
        """
        ID of the TaguchiMail activity record.
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
        Activity name.
        """
        return str(self.backing["name"])

    @name.setter
    def name(self, value):
        self.backing["name"] = value

    @property
    def type(self):
        """
        This is matched up with Template types to determine what to show the
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
    def target_lists(self):
        """
        This is a JSON array of list IDs to which the activity should be sent
        when queued.
        """
        return str(self.backing["target_lists"])

    @target_lists.setter
    def target_lists(self, value):
        self.backing["target_lists"] = value

    @property
    def target_views(self):
        """
        This is a JSON array of view IDs to which the activity distribution
        should be restricted.
        """
        return str(self.backing["target_views"])

    @target_views.setter
    def target_views(self, value):
        self.backing["target_views"] = value

    @property
    def approval_status(self):
        """
        Approval workflow status of the activity; JSON object containing a
        list of locked-in deployment setting used by the queue command.
        """
        return str(self.backing["approval_status"])

    @approval_status.setter
    def approval_status(self, value):
        self.backing["approval_status"] = value

    @property
    def deploy_datetime(self):
        """
        Date/time at which this activity was deployed (or is scheduled to
        deploy).
        """
        return str(self.backing["date"])

    @deploy_datetime.setter
    def deploy_datetime(self, value):
        self.backing["date"] = value

    @property
    def template_id(self):
        """
        The ID of the Template this activity uses.
        """
        return str(self.backing["template_id"])

    @template_id.setter
    def template_id(self, value):
        self.backing["template_id"] = value

    @property
    def campaign_id(self):
        """
        The ID of the Campaign to which this activity belongs.
        """
        return str(self.backing["campaign_id"])

    @campaign_id.setter
    def campaign_id(self, value):
        self.backing["campaign_id"] = value

    @property
    def throttle(self):
        """
        Maximum deployment rate of this message, in messages per minute. If 0,
        the activity is suspended. Web pages (an other pull messages) ignore
        this value.
        """
        return int(self.backing["throttle"])

    @throttle.setter
    def throttle(self, value):
        self.backing["throttle"] = value

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
        Activity status; leave None if not used.
        """
        return str(self.backing["status"])

    @property
    def latest_revision(self):
        """
        Latest activity revision content. If set, a new revision will be
        created upon activity create/update.
        """
        if len(self.backing["revisions"]) > 0:
            return ActivityRevision(self,
                revision=self.backing["revisions"][0])
        elif len(self.existing_revisions) > 0:
            return ActivityRevision(this,
                revision=self.existing_revisions[0])
        else:
            return None

    @latest_revision.setter
    def latest_revision(self, value):
        revision = dict(content=value.content)
        if len(self.backing["revisions"]) > 0:
            self.backing["revisions"][0] = revision
        else:
            self.backing["revisions"].append(revision)

    def update(self):
        """
        Saves this activity to the TaguchiMail database.
        """
        super(Activity, self).update()
        # Need to move the existing revisions to avoid re-creating the same
        # ones if this object is saved again.
        self.existing_revisions = self.backing["revisions"]
        self.backing["revisions"] = []

    def create(self):
        """
        Creates this activity in the TaguchiMail database.
        """
        super(Activity, self).create()
        # Need to move the existing revisions to avoid re-creating the same
        # ones if this object is saved again.
        self.existing_revisions = self.backing["revisions"]
        self.backing["revisions"] = []

    def proof(self, proof_list, subject_tag, custom_message):
        """
        Sends a proof message for an activity record to the list with the
        specified ID/to a specific list.

        proof_list: str/SubscriberList
            Indicates List ID of the proof list/the list to which the messages
            will be sent.
        subject_tag: str
            Displays at the start of the subject line.
        custom_message: str
            Contains a custom message which will be included in the proof
            header.
        """
        if isinstance(proof_list, str):
            data = [dict(id=self.record_id, list_id=proof_list,
                tag=subject_tag, message=custom_message)]
            self.context.make_request(self.resource_type, "PROOF",
                str(self.backing["id"]), json.dumps(data))
        else:
            self.proof(proof_list.record_id, subject_tag, custom_message)

    def request_approval(self, approval_list, subject_tag, custom_message):
        """
        Sends an approval request for an activity record to the list with the
        specified ID/to a specific list.

        approval_list: str/SubscriberList
            Indicates List ID of the approval list/the list to which the
            approval request will be sent.
        subject_tag:
            Displays at the start of the subject line.
        custom_message:
            Contains a custom message which will be included in the approval
            header.
        """
        if isinstance(approval_list, str):
            data = [dict(id=self.record_id, list_id=approval_list,
                tag=subject_tag, message=custom_message)]
            self.context.make_request(self.resource_type, "APPROVAL",
                str(self.backing["id"]), json.dumps(data))
        else:
            self.request_approval(approval_list.record_id, subject_tag,
                custom_message)

    def trigger(self, subscribers, request_content, test):
        """
        Triggers the activity, causing it to be delivered to a specified list
        of subscribers.

        subscribers: numeric list
            Contains subscriber IDs/subscribers to whom the message should be
            delivered.
        request_content: str
            XML content for message customization. The request_content
            document is available to the activity template's stylesheet, in
            addition to the revision's content. Should be None if unused.
        test: boolean
            Determines whether or not to treat this as a test send.
        """
        if isinstance(subscribers[0], str):
            data = [dict(id=self.record_id, test=1 if test else 0,
                request_content=request_content, conditions=subscribers)]
            self.context.make_request(self.resource_type, "TRIGGER",
                str(self.backing["id"]), json.dumps(data))
        else:
            subscriber_ids = []
            for s in subscribers:
                subscriber_ids.append(s.record_id)
            self.trigger(subscriber_ids, request_content, test)

    @staticmethod
    def get(context, record_id, parameters):
        """
        Retrieves a single Activity based on its TaguchiMail identifier.

        context: Context
            Determines the TM instance and organization to query.
        record_id: str
            Contains the list's unique TaguchiMail identifier.
        """
        results = json.loads(context.make_request("activity", "GET",
            record_id, parameters=parameters))
        rec = Activity(context)
        rec.backing = results[0]
        rec.existing_revisions = rec.backing["revisions"]
        # Clear out existing revisions so they're not sent back to the server
        # on update.
        rec.backing["revisions"] = []
        return rec

    @staticmethod
    def get_with_content(context, record_id, parameters):
        """
        Retrieves a single Activity based on its TaguchiMail identifier, with
        its latest revision content.

        context: Context
            Determines the TM instance and organization to query.
        record_id: str
            Contains the list's unique TaguchiMail identifier.
        """
        new_params = dict(revision="latest")
        return Activity.get(context, record_id, new_params)

    @staticmethod
    def find(context, sort, order, offset, limit, query):
        """
        Retrieves a list of Activities based on a query.

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
        results = json.loads(context.make_request("activity", "GET",
            parameters=parameters, query=query))
        records = []
        for result in results:
            rec = Activity(context)
            rec.backing = result
            rec.existing_revisions = rec.backing["revisions"]
            # Clear out existing revisions so they're not sent back to the
            # server on update.
            rec.backing["revisions"] = []
            records.append(rec)
        return records
