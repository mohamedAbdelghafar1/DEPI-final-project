from azure.storage.blob import BlobServiceClient
import os

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = "raw-data"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

file_path = "dataset\\raw-data.csv"

with open(file_path, "rb") as data:
    container_client.upload_blob(name="raw-data.csv", data=data, overwrite=True)

print("File uploaded successfully.")