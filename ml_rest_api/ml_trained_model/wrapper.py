"""This module implements the TrainedModelWrapper class."""
import os
import os.path
import importlib
from threading import Thread
from ml_rest_api.settings import get_value


class TrainedModelWrapper:
    """TrainedModelWrapper class acts as adapter for programmatically chosen ML trained model
    module. The init(), run() and sample() methods call the module's identically named methods."""

    def __init__(self):
        """Initialise everything to None, particularly init, run, sample and ready methods."""
        self._init = None
        self._run = None
        self._sample = None
        self.initialised = False
        self.module_name = None
        self.module = None

    def load(self, module_name):
        """Loads a Python module, binding the init, run and sample callable methods."""

        def bind_funct(funct_name):
            """Binds a named attibute if it exists and it's callable"""
            if hasattr(self.module, funct_name):
                funct = getattr(self.module, funct_name)
                if callable(funct):
                    return funct
            return None

        self.module_name, _ = os.path.splitext(module_name)
        self.module = importlib.import_module(
            "ml_rest_api.ml_trained_model." + self.module_name
        )
        self._init = bind_funct("init")
        self._run = bind_funct("run")
        self._sample = bind_funct("sample")

    @staticmethod
    def find_first_module():
        """Finds first available module (the first Python module found in the current dir that is
        not this wrapper or starts with __). Returns the name minus .py extension"""
        for filename in os.listdir(os.path.dirname(__file__)):
            if (
                len(filename) >= 2
                and filename[0:2] != "__"
                and filename != os.path.basename(__file__)
            ):
                module, extension = os.path.splitext(filename)
                if extension == ".py":
                    return module
        return None

    def load_default_module(self):
        """Loads a module, chosen either by getting the name from TRAINED_MODEL_MODULE_NAME env var
        or from the settings file. If module is not found in env var or settings, find it by calling
        load_first_module()"""
        env_model_name = get_value("TRAINED_MODEL_MODULE_NAME")
        if not env_model_name:
            env_model_name = self.find_first_module()
        if env_model_name:
            self.load(env_model_name)

    def ready(self):
        """Returns wther the model it's correctly initialised and a wrapped run() method can be called"""
        return self._run and self.initialised

    def multithreaded_init(self):
        """Calls self.init() to load the model in a separate thread."""
        if self._init:
            Thread(target=self.init).start()

    def init(self):
        """Calls the wrapped init() method if it's assigned."""
        if self._init and not self.initialised:
            self._init()
            self.initialised = True

    def run(self, data):
        """Calls the wrapped run() method if it's assigned."""
        if self._run:
            return self._run(data)
        return None

    def sample(self):
        """Calls the wrapped sample() method if it's assigned."""
        if self._sample:
            return self._sample()
        return None


trained_model_wrapper = TrainedModelWrapper()
trained_model_wrapper.load_default_module()
