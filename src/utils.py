from typing import Callable

# def get_client_for_version(version=1):
#         versioned_clients = {
#             1: boto3_wrapper.client("kms", {
#                 "region_name": constants.AWS_REGION_NAME,
#                 "aws_access_key_id": aws_access_key_id,
#                 "aws_secret_access_key": aws_secret_access_key,
#             })
#         }
#         return versioned_clients[version]

# class ProjectIntegrationSettingsProperty:

#     encryption_access_key_id = constants.ENCRYPTION_ACCESS_KEY_ID
#     encryption_key_id = constants.ENCRYPTION_KEY_ID
#     encryption_secret_access_key_id = constants.ENCRYPTION_SECRET_ACCESS_KEY_ID

#     user_id = constants.USER_ID
#     project_id = constants.PROJECT_ID
#     integration_id = constants.INTEGRATION_ID

#     def __init__(self):
#         self.encryption_service_kwargs = {
#             "aws_access_key_id": self.encryption_access_key_id,
#             "aws_secret_access_key": None,
#         }


#     def encrypt():
#         pass

#     def decrypt(data):
#         client = get_client_for_version(1)

def is_string(data) -> bool:
    """
    Takes an object and returns if that object is a string type.

    Parameters:
      data (obj): Object to test
    """
    return isinstance(data, str)

def is_bytes(data) -> bool:
    """
    Takes an object and returns if that object is a bytes type.

    Parameters:
      data (obj): Object to test
    """
    return isinstance(data, (bytes, bytearray))

def _simple_encoder(encoder) -> Callable:
    """
    Takes an encoder method and returns back an encode method that uses the encoder.

    Parameters:
      encoder (func): Encoder method to employ
    """

    def encode(original):
        """
        Takes an original string object and returns its encoded form based on the supplied encoder.

        Parameters:
          original (str): String to encode
        """
        if original is None:
            return None

        if is_string(original):
            return original.encode(encoder)

        return original

    return encode

def _simple_decoder(decoder) -> Callable:
    """
    Takes a decoder method and returns back a decode method that uses the decoder.

    Parameters:
      decoder (func): Decoder method to employ
    """

    def decode(original, ignore_errors=False):
        """
        Takes an original byte object and returns its decoded form based on the supplied decoder.

        Parameters:
          original (bytes): Byte array to decode
        """
        errors = "ignore" if ignore_errors else "strict"

        if original is None:
            return None

        if is_bytes(original):
            return original.decode(decoder, errors)

        return original

    return decode

encode_utf8 = _simple_encoder("utf-8")
decode_utf8 = _simple_decoder("utf-8")
