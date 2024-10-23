from __future__ import absolute_import
import boto3
from botocore import exceptions as botocore_exceptions

def client(service_name, **kwargs):
    """Get a boto3 client for a given service using either local AWS credentials or pistachio credentials.

    :param service_name: str - the name of the AWS service client to create
    :param kwargs: keyword arguments to pass to boto3.client. See
    http://boto3.readthedocs.io/en/latest/reference/core/session.html#boto3.session.Session.client
    for details.
    :return: Service client instance
    """
    # Try to use the Pistachio credentials for AWS.

    # Internally, by default boto3 uses a global session, since the session has mutable internal state, this does not
    # play nicely with threadsafe: true, due to this a new session is allocated for every client.
    session = boto3.Session()
    try:
        return session.client(service_name, **kwargs)
    # If that fails, try to use local credentials. If that fails, raise up.
    except botocore_exceptions.ClientError as e:
        # If the provided credentials are invalid (or empty), try to use local credentials.
        #   Drop access and secret keys before creating the client to force boto3 to use local credentials.
        if "InvalidAccessKeyId" in str(e):
            _ = kwargs.pop("aws_access_key_id")
            _ = kwargs.pop("aws_secret_access_key")
            return session.client(service_name, **kwargs)
