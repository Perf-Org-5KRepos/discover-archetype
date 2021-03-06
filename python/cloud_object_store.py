import ibm_boto3
from ibm_botocore.client import Config, ClientError


class CloudObjectStore:

    DEFAULT_ENDPOINT = \
        'https://s3.us-east.cloud-object-storage.appdomain.cloud'

    DEFAULT_AUTH_ENDPOINT = \
        'https://iam.cloud.ibm.com/identity/token'

    '''
    Interface to IBM Cloud Object Store, typical values:
        bucket_name:  name of your storage bucket
        api_key: your API key
            (go to Cloud Storage dashboard -> Service credentials)
        resource_crn: your bucket CRN
            (go to your bucket -> Configuration: Bucket instance CRN)
        endpoint: for external access,
            "https://s3.us-east.cloud-object-storage.appdomain.cloud"
        endpoint: for internal access,
            "https://s3.private.us-east.cloud-object-storage.appdomain.cloud"
        auth_endpoint: "https://iam.cloud.ibm.com/identity/token"
    '''
    def __init__(self, bucket_name,
                 api_key,
                 resource_crn,
                 endpoint=DEFAULT_ENDPOINT,
                 auth_endpoint=DEFAULT_AUTH_ENDPOINT,
                 ):
        self.bucket_name = bucket_name
        self.COS_API_KEY_ID = api_key
        self.COS_RESOURCE_CRN = resource_crn
        self.COS_ENDPOINT = endpoint
        self.COS_AUTH_ENDPOINT = auth_endpoint

        self.cos = ibm_boto3.resource(
            "s3",
            ibm_api_key_id=self.COS_API_KEY_ID,
            ibm_service_instance_id=self.COS_RESOURCE_CRN,
            ibm_auth_endpoint=self.COS_AUTH_ENDPOINT,
            config=Config(signature_version="oauth"),
            endpoint_url=self.COS_ENDPOINT
        )

    def get_bucket_contents(self):
        try:
            files = self.cos.Bucket(self.bucket_name).objects.all()
            return [file.key for file in files]
        except ClientError as be:
            print("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            print("Unable to retrieve bucket contents: {0}".format(e))

    def get_item(self, item_name):
        try:
            file = self.cos.Object(self.bucket_name, item_name).get()
            return file["Body"].read()
        except ClientError as be:
            print("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            print("Unable to retrieve file contents: {0}".format(e))

    def create_item(self, item_name, file_text):
        print("Creating new item: {0}".format(item_name))
        try:
            self.cos.Object(self.bucket_name, item_name).put(
                Body=file_text
            )
        except ClientError as be:
            print("CLIENT ERROR: {0}\n".format(be))
        except Exception as e:
            print("Unable to create text file: {0}".format(e))
