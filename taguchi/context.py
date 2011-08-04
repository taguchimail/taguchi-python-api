import json
import urllib
import httplib

class Context(object):
    """
    Represents a TaguchiMail connection. Must be created prior to
    instantiation of any other TaguchiMail classes, as it's a required
    parameter for their constructors.
    """

    def __init__(self, hostname, username, password, organization_id):
        """
        The Context constructor.

        hostname: str
            Contains the hostname (or IP address) of the TaguchiMail instance
            to connect with.
        username: str
            Contains the username (email address) of an authorized user.
        password: str
            Contains the password of an authorized user.
        organization_id: str
            Indicates the organization ID to be used for creation of
            new objects. The username supplied must be authorized to access
            this organization.
        """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.organization_id = organization_id
        self.base_uri = "/admin/api/" + str(organization_id)

    def make_request(self, resource, command, record_id=None, data=None,
                     parameters=None, query=None):
        """
        Makes a TaguchiMail request with a given resource, command, parameters
        and query predicates.

        resource: str
            Indicates the resource.
        command: str
            Indicates the command to issue to the resource.
        record_id: str
            Indicates the ID of the record to operate on, for record-specific
            commands.
        data: str
            Contains the JSON-formatted record data for the command, if
            required by the command type.
        parameters: dict
            Contains additional parameters to the request. The supported
            parameters will depend on the resource and command, but commonly
            supported parameters include:
            * sort: one of the resource's fields, used to sort the result set;
            * order: either 'asc' or 'desc', determines whether the result set
              is sorted in ascending or descending order;
            * limit: positive non-zero integer indicating the maximum returned
              result set size (default to 1);
            * offset: either 0 or a positive integer indicating the position
              of the first returned result in the result set (default to 0).
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
        qs = self.base_uri + "/" + resource + "/"
        if record_id is not None:
            qs += record_id
        qs += "?_method=" + urllib.quote(command)
        qs += "&auth=" + urllib.quote(self.username + "|" + self.password)
        if query is not None:
            for predicate in query:
                qs += "&query=" + urllib.quote(predicate)
        if parameters is not None:
            for key, value in parameters.items():
                qs += "&" + urllib.quote(key) + "=" + urllib.quote(value)

        conn = httplib.HTTPSConnection(self.hostname, timeout=60)
        method = "GET" if command == "GET" else "POST"
        # Authenticate always required, so don't wait for a 401 beforehand.
        # Work in JSON, it's smaller and faster at the TM end. In addition the
        # stats resource doesn't have an XML serialization available (tabular
        # data in XML is nasty). Set a user-agent so we can track any errors
        # occurring a little more easily.
        headers = dict(
            PreAuthenticate="true",
            Accept="application/json",
            UserAgent="TMAPIv4 python wrapper")
        # Post data if it was supplied.
        if (data is not None and len(data) > 0):
            headers.update({
                "Content-Type": "application/json",
                "Content-Length": len(data)})
        conn.request(method, qs, data, headers)
        rep = conn.getresponse()
        result = rep.read()
        conn.close()
        return result
