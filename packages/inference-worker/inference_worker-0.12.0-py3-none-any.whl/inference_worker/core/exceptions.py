class InferenceError(Exception):
    _default_message = "Inferencing Error: Something went wrong"
    _default_code = "inference_error"
    def __init__(self, message, code = None):
        self.message = message
        self.code = code

        if self.message is None:
            self.message = self._default_message

        if self.code is None:
             self.code = self._default_code