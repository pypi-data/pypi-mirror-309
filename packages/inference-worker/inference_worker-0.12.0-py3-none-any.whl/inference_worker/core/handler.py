from .abstraction import InferenceResult, ModelBuilder, Model
from .exceptions import InferenceError
import importlib, json, os, pathlib, multiprocessing, requests, sys
from .input import Message

CONFIG_FILE_PATH = pathlib.Path(os.getcwd()) / 'config.json'

class InferenceHandler:
    def __init__(self):
        self.model_builder_class = self._load_implementation(CONFIG_FILE_PATH)

    def _load_implementation(self, config_path):
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        sys.path.append(os.getcwd())
        module_path, class_name = config["model_builder_class"].rsplit('.', 1)
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    

    def handle(self, input: Message):
        # Create a queue to communicate between processes
        inputFiles = input.get_input_files()
        modelArtifacts = input.get_model_artifacts()
        args = input.get_args()

        try:
            modelBuilder: ModelBuilder = self.model_builder_class()
            model: Model = modelBuilder.build(modelArtifacts)
            result: InferenceResult = model.infer(inputFiles, **args)
            self._handle_success(input, result)
            print("========== Inference Successful: ===========")
            print(result)
        except InferenceError as e:
            self._handle_error(input, e.code, e.message)
            print("========== Inference Failed ===========")
            print(e)



    def _handle_success(self, input: Message, result: InferenceResult):
        filename = os.path.basename(result['output'])
        metadta = result['metadata']
        multipart_form_data = {
            'outputFile': (filename, open(result['output'], 'rb')),
        }
        response = requests.post(
            input._outputCallback, 
            files=multipart_form_data,
            data={'metadata': json.dumps(metadta)}
        )

        if response.status_code != 200:
            print(response.content)
            print(response.status_code, response.reason)
        else:
            print('==========SUCESS (Result)===========')
            print(response.json())

    def _handle_error(self, input: Message, code, message):
        
        data = {
            'code': code,
            'message': message
        }

        response = requests.post(input._errorCallback, json=data)
        if (response.status_code != 200):
            print(response.content)
            print(response.status_code, response.reason)

        else:
            print('==========SUCESS (Error)===========')
            print(response.json())


