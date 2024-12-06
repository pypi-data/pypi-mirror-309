import requests, typing, os
from .storage import default_storage

class InferenceRequest:

    def __init__(self, id: str, inputFiles: list[str], modelArtifacts: list[str], args: dict):
        self.id = id
        self.inputFiles = inputFiles
        self.modelArtifacts = modelArtifacts
        self.args = args


class Message:
    def __init__(self, *, outputCallback, errorCallback, request: InferenceRequest):
        self._outputCallback = outputCallback
        self._errorCallback = errorCallback
        self._request = request
    
    @property
    def temporary_files_directory(self):
        return default_storage.get_temporary_files_directory()
    
    def download_file(self, url) -> str:
        response = requests.get(url)

        if response.status_code == 200:
            filename = url.split('/')[-1]
            file_path = os.path.join(self.temporary_files_directory, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'wb') as file:
                file.write(response.content)

            return file_path
            
        raise Exception(f'Failed to download: {url}')
    
    def get_input_files(self) -> typing.List[str]:
        files = []

        for inputFileUrl in self._request['inputFiles']:
            filePath = self.download_file(inputFileUrl)
            files.append(filePath)
            
        return files

    def get_model_artifacts(self) -> typing.List[str]:
        files = []
        
        for inputFileUrl in self._request['modelArtifacts']:
            filePath = self.download_file(inputFileUrl)
            files.append(filePath)
            
        return files
    
    def get_args(self) -> dict:
        return self._request['args']
    
    @property
    def request(self) -> InferenceRequest:
        return self._request

    @property
    def outputCallback(self) -> str:
        return self._outputCallback
    
    @property
    def errorCallback(self) -> str:
        return self._errorCallback