import constants
import logging
import base64
from utils import encode_utf8, decode_utf8
import boto3_wrapper
import json

ENCRYPTED_JSON_METADATA_KEY = "encrypted_json_metadata"

encryption_key_id = constants.ENCRYPTION_KEY_ID
encryption_service_kwargs = {
    "aws_access_key_id": constants.ENCRYPTION_ACCESS_KEY_ID,
    "aws_secret_access_key": constants.ENCRYPTION_SECRET_ACCESS_KEY_ID,
}

class ProjectIntegrationSettingsPropertyDecode:

    def __init__(self):
        self.BACKEND_VERSION = 1
        self._client_kwargs = {
            "region_name": constants.AWS_REGION_NAME,
            "aws_access_key_id": constants.ENCRYPTION_ACCESS_KEY_ID,
            "aws_secret_access_key": constants.ENCRYPTION_SECRET_ACCESS_KEY_ID,
        }
    
    def _get_client_for_version(self, version=None):
        """Abstraction to get a client by version."""
        if version is None:
            version = self.BACKEND_VERSION

        versioned_clients = {
            1: boto3_wrapper.client("kms", **self._client_kwargs),
        }
        return versioned_clients[version]

    def decypt(self, value):
        if ENCRYPTED_JSON_METADATA_KEY not in value:
            logging.debug("{} not in value. Not decrypting.".format(ENCRYPTED_JSON_METADATA_KEY))
            return None

        logging.debug("Decrypting a value for")

        value_to_decrypt = base64.b64decode(encode_utf8(value[ENCRYPTED_JSON_METADATA_KEY]["ciphertext"]))
        decrypt_version = value[ENCRYPTED_JSON_METADATA_KEY]["version"]

        client = self._get_client_for_version(version=decrypt_version)
        aws_response = client.decrypt(CiphertextBlob=value_to_decrypt)

        plaintext_data = aws_response["Plaintext"]
        plaintext_data = json.loads(decode_utf8(plaintext_data))
        return plaintext_data


if __name__ == "__main__":
    decode_integration = ProjectIntegrationSettingsPropertyDecode()

    # prod (update the constants values with respective environments
    # value_to_decode = {"encrypted_json_metadata":{"version":1,"ciphertext":"AQICAHhpu5TRG+aUePxRX1SRvyzC37p2/mQo4qW4K1Nm1hblWwHqnar7tjnsqOmPeCzChKqIAAACIDCCAhwGCSqGSIb3DQEHBqCCAg0wggIJAgEAMIICAgYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAzS9NfFBWVa6KYUPVYCARCAggHTJxE9ZC2aeIbkoWUb/fLstb/9/lenahlTaNXQdlwdmBTjZuRFKHU6h0VvCzNDCN9ABBJq4yS3SG3BVgDKUgQY4fJUlNFDWirYf+vul6Z70tcOc2R2GRmlWr9b9fo29b2tKHttEYtg8CePiS4aUfz2RLY674WyNHHZuLpYP+KdkgQk6kV90EGwCK0VThco5YZpbvjsLv1c5Kmtu7D6d9j+RV6KqiYLFxlMSphPwRTZVu6ezcviBGWqgIPBl6OtPZuiYf6X6mGz0LSzwRp7cxS+e5Ny7/hRqMD0C1OT+uWsxTcPuxAvzC+5ZfdtyrY0ELmyHD21r2WKbOenKOkqjkbAfARy56UERlBW3ixl2hTFPvWPCfb5KpLCa51j3QIY4F0Rc39BrJCSJOmqeG1b3a5ck85LoRwKT3D3rg44/IVpshAl7/YuMiUdQQUw0X65pYT0BuL44Y66DK6o4mE3HdtxUQleI921gHx6f1pAv4gWIbEYP63Pn0lPteFwmbusoUW+ZCFkTtRDrhFEx/TvdNEiHD88NdZZvsEs2L136b+QY8qXockaMp3XyFubxmi55G7uSBsSR4BPb15nM+/oqofXiybgs1wW8iit5jNyHePpVEU0674="}}
    # value_to_decode = {"encrypted_json_metadata":{"version":1,"ciphertext":"AQICAHhpu5TRG+aUePxRX1SRvyzC37p2/mQo4qW4K1Nm1hblWwHqnar7tjnsqOmPeCzChKqIAAACIDCCAhwGCSqGSIb3DQEHBqCCAg0wggIJAgEAMIICAgYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAzS9NfFBWVa6KYUPVYCARCAggHTJxE9ZC2aeIbkoWUb/fLstb/9/lenahlTaNXQdlwdmBTjZuRFKHU6h0VvCzNDCN9ABBJq4yS3SG3BVgDKUgQY4fJUlNFDWirYf+vul6Z70tcOc2R2GRmlWr9b9fo29b2tKHttEYtg8CePiS4aUfz2RLY674WyNHHZuLpYP+KdkgQk6kV90EGwCK0VThco5YZpbvjsLv1c5Kmtu7D6d9j+RV6KqiYLFxlMSphPwRTZVu6ezcviBGWqgIPBl6OtPZuiYf6X6mGz0LSzwRp7cxS+e5Ny7/hRqMD0C1OT+uWsxTcPuxAvzC+5ZfdtyrY0ELmyHD21r2WKbOenKOkqjkbAfARy56UERlBW3ixl2hTFPvWPCfb5KpLCa51j3QIY4F0Rc39BrJCSJOmqeG1b3a5ck85LoRwKT3D3rg44/IVpshAl7/YuMiUdQQUw0X65pYT0BuL44Y66DK6o4mE3HdtxUQleI921gHx6f1pAv4gWIbEYP63Pn0lPteFwmbusoUW+ZCFkTtRDrhFEx/TvdNEiHD88NdZZvsEs2L136b+QY8qXockaMp3XyFubxmi55G7uSBsSR4BPb15nM+/oqofXiybgs1wW8iit5jNyHePpVEU0674="}}
    # value_to_decode = {"encrypted_json_metadata":{"version":1,"ciphertext":"AQICAHho2wLY/uhi/G1gWbeDqD2A2X58QFrAOWpl4RQNmcfPXgFeFcgDIzrFJX/3XT3rPO9kAAACOzCCAjcGCSqGSIb3DQEHBqCCAigwggIkAgEAMIICHQYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAwCJk1tyq96dl41xiACARCAggHuSq3JGzP5VmWQGQwqejiEYYamz43bx5TA4wIJYNU6ghceVyVJTtX1Bq2OJDNQHUlzWGkTTP5VkKfuxhUtvBjeO522jYcKO8gjIQRjLr38fewYbHwWbG8rjgRTsGARmvIzGHHyFlEdEOwttSmpGgQHFWvzW6W6TO98a1nDxXhV7YAmrtrnVWcOc+M0DiU9li1/w+AHjW64EMFzsBYTHGE1I/5kyKFTgAwRAq4SFFeAxB7WkQLI1xBexulBy873gYoRXfxtdrgdXiEuC0zSlZtxiBYkbwMiFjiGi89aS5cdev+4YN9ZlkAbFtrF+9jUUwCbtEOuRMFj6XjV9gIx2TuP59AAKq0T7fbzDbkHyhMAWgAPB+vXEqsK+2effgVzaMwiA5xhUWOq7OgX2MXcIoI3BG2Y0Fnu/n6Su/RLrlB4ux2MlBUrs3pcUfxIzu39Hr4TWMCiB5RIXpphfF8yNaHh3S8j257qrRVVHuq5uROcqHd9MO9F2DiAAFCZzDXIU5gDGD6bT44EksvVWhsEfstvxrQedlufNW8XcL02f9C92/mHL/bce1UdLD71uqQwfpRUcepXO4Y39Dgx0xeudS8hj/Fj45d1HBNZuTu3lXzuOqYdDYcWaA/euIq+7w5io37d04dS6LwkWUsPgyZvBh0="}}
    # value_to_decode = {"encrypted_json_metadata":{"version":1,"ciphertext":"AQICAHho2wLY/uhi/G1gWbeDqD2A2X58QFrAOWpl4RQNmcfPXgF0lZUtRPCDg4YAiaKLfF7VAAACIDCCAhwGCSqGSIb3DQEHBqCCAg0wggIJAgEAMIICAgYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAxJzE/0cO/q40uMkw8CARCAggHTerrf13Z1plqbcQn58T1YiZab5vN50D+uxFxp1riRSik+eqMPkgZjGGT95/1PgNxUAYEqbWLByn3a5d9G3idr6Za+xHiB0IL/Idwbkv6+RNv9d3RJS/EK+NPFjeGIv9vZSu92nCi91GEus+4E8lN+u69lVW+ooDbrxtT7iHo1YCan2O9+3/gt4On3lNCmShTOFVc5Oh/zao7H3Og6Kf0BIKnic0zT7x45Mn6YLfH9SbQpKWysAhgTOq/BuM+oiLIBFqD5QCzxQ/bBh9BxPoJonGfIClLSqKisMq2/Ds9tBPzfukY7AFJApvrMf+2f19rgbBRGl117GzD+Q/+NGM5K3aao+vCp9Xf+ZXa7JA4flxDQwWR394ZBoHC0RxWBhasgmhusxfoA5QGcUHBczaed/BNhFy8Vr+b6Ne+TfzJyFNXJ4T3bk0686sVEkiusNo2KdD8iSaFN+AhudvoyDQmYludxRMccF27JgiBuEFF3P5iA+UB2M9+6cF4rDnQCsaL56muHB5oo1ZqD6QjA1rHjxJJ0DAeHNPMRDNqj5fiU874cF4Us0San/0sWdi4c/CePHrXkPitOZjqDPFoyXduYfNFG+SrsGGdvlF+JoxJQdvHN+M8="}}
    value_to_decode = {"encrypted_json_metadata": {"version": 1, "ciphertext": "AQICAHhpu5TRG+aUePxRX1SRvyzC37p2/mQo4qW4K1Nm1hblWwGYpZRoCyQKCuB74EOSzb3uAAACPzCCAjsGCSqGSIb3DQEHBqCCAiwwggIoAgEAMIICIQYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAxRRMhEYMnJXidPydICARCAggHyqgVTFvWOmXPMmYLd0dZT/IbJmh8csuT5b414480qVa2G7Y7I1eyr9CPRLoKDRZ7yC308toFkWLZFepwvy0eSqkGjATaDDYgTm/+Icmzi54+FA2TK8zm/2uDbjgvoOCXjNEQaUQAER+Yn074nAhJ/bhEPox2wQV8MGdVRH7PoC+bDtHd3d2qhBqYji6PWwcNoIsGIvYc8ZCTVu5RlSsMBBtKhVBVjTwn6GLz8s3pI4CZ993TgpuCj+mR1O0q0wy+Ot7l2rtlirQqr+4CIbGqdyfNcUUwRcWAYN/bovtA961nNdosB6hTWb3vgZvNVo6WxiySev3FZJK23HbGQRPKgcgpsmtHQ41vi+76XsZ3bZwRhfrWlbQ5U7irbXWYDeaDfNa7sRQKcMGUTSObv27iXEYl4P95SFWYwjYQe+URiDP+VW7XwQtFT+nPZUF1ku8rqQjNxnkhmxUWGbLwKiQM9hxrENgaB8pZsMHPK1Y0A/KHGjZDfbYR/TrLqK81IUooUiO9ctYaArgGTK961dUafkSfcupTo8XMOZSKHipQ/u8kP48aMfvycSwBguCT2UIXDyelHxfvUigW1ImBIWn7jhrAhyWhYMZDWZFfUoBKYiJM//Tkw1Zls/ZvVT2+EHwV1y97zB4iW7zuXedvHNa+6uUNa"}}

    # develrc  (update the constants values with respective environments
    # value_to_decode = {"encrypted_json_metadata":{"version":1,"ciphertext":"AQICAHho2wLY/uhi/G1gWbeDqD2A2X58QFrAOWpl4RQNmcfPXgFeFcgDIzrFJX/3XT3rPO9kAAACOzCCAjcGCSqGSIb3DQEHBqCCAigwggIkAgEAMIICHQYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAwCJk1tyq96dl41xiACARCAggHuSq3JGzP5VmWQGQwqejiEYYamz43bx5TA4wIJYNU6ghceVyVJTtX1Bq2OJDNQHUlzWGkTTP5VkKfuxhUtvBjeO522jYcKO8gjIQRjLr38fewYbHwWbG8rjgRTsGARmvIzGHHyFlEdEOwttSmpGgQHFWvzW6W6TO98a1nDxXhV7YAmrtrnVWcOc+M0DiU9li1/w+AHjW64EMFzsBYTHGE1I/5kyKFTgAwRAq4SFFeAxB7WkQLI1xBexulBy873gYoRXfxtdrgdXiEuC0zSlZtxiBYkbwMiFjiGi89aS5cdev+4YN9ZlkAbFtrF+9jUUwCbtEOuRMFj6XjV9gIx2TuP59AAKq0T7fbzDbkHyhMAWgAPB+vXEqsK+2effgVzaMwiA5xhUWOq7OgX2MXcIoI3BG2Y0Fnu/n6Su/RLrlB4ux2MlBUrs3pcUfxIzu39Hr4TWMCiB5RIXpphfF8yNaHh3S8j257qrRVVHuq5uROcqHd9MO9F2DiAAFCZzDXIU5gDGD6bT44EksvVWhsEfstvxrQedlufNW8XcL02f9C92/mHL/bce1UdLD71uqQwfpRUcepXO4Y39Dgx0xeudS8hj/Fj45d1HBNZuTu3lXzuOqYdDYcWaA/euIq+7w5io37d04dS6LwkWUsPgyZvBh0="}}
    # value_to_decode = {"encrypted_json_metadata":{"version":1,"ciphertext":"AQICAHi84NhhSuEy5sMc6IsL1JKEpjxOjNEYB/1OA+iMg6oVhAHqu9QXMKr6Nk0IkAexjLIMAAACIDCCAhwGCSqGSIb3DQEHBqCCAg0wggIJAgEAMIICAgYJKoZIhvcNAQcBMB4GCWCGSAFlAwQBLjARBAxt7YT4iWthxmF57VMCARCAggHTfzVhamcNfx96scO+TStfUsgjP6ee9XBZOKKg2okkSlHXfV7ce7kbaCvGGk7ec23ufQRzS+ZmsERemh5Q77lvcth4vYcqY6HUs7O0dgHmm0TalsdA/lVISlURwJWS6AB72nDBhgi6sc0kACR8J+q/BM0q+hVoyQAKzwJ+ugsixI+bMqxn1WN4VroVSg24zF0vQvfw/G5orrdHqNtmlov9y/Q3yoD/ABeqNt9f4e/kktmcqcH1v7+UUfQeWJgwFXwjpJQjxzY96smslmuAlkBNVuUyJCn28g50ENbmqa8vJPtdgInXOCJ/7l2y84Gest4CnwDHiprh8UUQj0CTK30um2qmUBcl9odeSwCkTIR3+czZtZ7S3XpEPWhiOdW0LSD3foKw4+ig49IZ8R8sPh02qj5Poa3NcteisywdR2TYuQj/dFIvTxjFHtesIVQb+klkQ2BgOP3tWPkSBvuS32ubEDz+EGFV5MXmHfQb6H9xI8jWDqIELeqSXS4C26BK9A6FUT1e8uAzz3MERtPtuVoN8sGmmqispVu9AxoTaC7jLRUsqS4LOkwPAkSWXcdTwd97U4wVFETe1cqaV+Lrdqzc8g7FlB6KZx/nTq1/csHzRkrjz0U="}}

    plaintext_data = decode_integration.decypt(value_to_decode)
    print(plaintext_data)
