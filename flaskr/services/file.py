from datetime import datetime

from azure.core.exceptions import AzureError

from flaskr.cloud.azure import Azure
from flaskr.cloud.drive import GoogleDrive
from flaskr.models.file_transfer import FileTransferModel


class FileModelService:
    def init(self):
        self.google_drive = GoogleDrive()
        self.azure = Azure()

    def transfer_files(self):
        container_client = self.azure.connection_azure()
        files_drive = self.google_drive.list_files().get('files')

        if not files_drive:
            print("Nenhum arquivo encontrado no Google Drive.")
            return

        transfers = [] 

        for item in files_drive:
            file_name = item.split("(")[0].strip()
            file_id = item.split("(")[1].replace(")", "")
            file_content = self.google_drive.download_file(file_id)

            if not isinstance(file_content, bytes):
                file_content = bytes(str(file_content), 'utf-8')

            blob_client = container_client.get_blob_client(container='midall', blob=file_name)

            try:
                blob_client.upload_blob(file_content, overwrite=True)
                print(f"Arquivo {file_name} transferido com sucesso para o Azure Blob Storage!")

                self.google_drive.remove_files(file_id)
                print(f"Arquivo {file_name} deletado do Google Drive!")

                transfer = FileTransferModel()
                transfer.name = file_name
                transfer.size = len(file_content)
                transfer.format = file_name.split(".")[-1]
                transfer.date_upload = datetime.now()
                transfer.data_transfer = datetime.now()

                transfers.append(transfer) 

            except AzureError as ex:
                print('Um erro ocorreu durante o upload do arquivo: {}'.format(ex))


        for transfer in transfers:
                transfer.save()
                transfers = []