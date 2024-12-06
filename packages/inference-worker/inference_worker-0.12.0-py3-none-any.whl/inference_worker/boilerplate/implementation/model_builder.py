from inference_worker.core import abstraction

class ModelBuilder(abstraction.ModelBuilder):

    def build(self, model_file_paths, *args, **kwargs):
        raise NotImplementedError()
        

model_builder_class = ModelBuilder