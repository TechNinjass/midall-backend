import os
import pickle

from azure.storage.blob import BlobServiceClient

class Azure:
    def __init__(self):
        self.account_name = None
        self.account_key = None
        self.container_name = None

    def connection_azure(self, account_name=None, account_key=None, container_name=None, use_pickle=False):
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name
        
        #fix line
        connect_str = ""

        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        if not use_pickle:
            credentials = {"account_name": self.account_name, "account_key": self.account_key, "container_name": self.container_name}
            with open("credentialsAzure.pickle", "wb") as f:
                pickle.dump(credentials, f)

        return blob_service_client

    def list_files(self):
        with open("credentialsAzure.pickle", "rb") as f:
            credentials = pickle.load(f)

        #fix line
        connect_str = ""
        
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        container_client = blob_service_client.get_container_client(credentials['container_name'])

        blob_list = container_client.list_blobs()

        file_names = []
        for blob in blob_list:
            file_names.append(blob.name)

        return file_names