from typing import TypedDict

FilePath = str


InferenceResult = TypedDict('InferenceResult', {
    'output': FilePath,
    'metadata': dict
})

InferenceMetadata = TypedDict('InferenceResult', {
    'input_files': list[list[str]],
    'model_artifacts': list[list[str]]
})

     
class Model:
    """
      An object that can infer or predict
      Contains every knowledge about performing the inference given an input
    """
    def infer(self, input_file_paths: list[FilePath], *args, **kwargs) -> InferenceResult:
        raise NotImplementedError()
    

class ModelBuilder:
    """
        An object that can build the inference model given a list of model artifacts
        contains every logic that it needs to build the model
    """
    def build(self, model_file_paths: list[FilePath], *args, **kwargs) -> Model:
        raise NotImplementedError()

   
