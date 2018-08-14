"""This module implements the TrainedModelWrapper class."""
import os
import os.path
import importlib
from ml_rest_api.settings import get_value

class TrainedModelWrapper:
    """TrainedModelWrapper class acts as adapter for programmatically chosen ML trained model
    module. The init(), run(), ready() and sample() methods call the module's identically named
    methods."""

    def __init__(self):
        """Initialise everything to None, particularly init, run, sample and ready methods."""
        self._init = None
        self._run = None
        self._sample = None
        self._ready = None
        self.initialised = False
        self.module_name = None
        self.module = None

    def load(self, module_name):
        """Loads a Python module, finding the init, run, sample and ready methods."""
        self.module_name, _ = os.path.splitext(module_name)
        self.module = importlib.import_module('ml_rest_api.ml_trained_model.' + self.module_name)
        if hasattr(self.module, 'init'):
            self._init = getattr(self.module, 'init')
        if hasattr(self.module, 'run'):
            self._run = getattr(self.module, 'run')
        if hasattr(self.module, 'sample'):
            self._sample = getattr(self.module, 'sample')
        if hasattr(self.module, 'ready'):
            self._ready = getattr(self.module, 'ready')

    @staticmethod
    def find_first_module():
        """Finds first available module (the first Python module found in the current dir that is
        not this wrapper or starts with __). Returns the name minus .py"""
        for filename in os.listdir(os.path.dirname(__file__)):
            if len(filename) >= 2 and filename[0:2] != '__' and \
                filename != os.path.basename(__file__):
                module, extension = os.path.splitext(filename)
                if extension == '.py':
                    return module
        return None

    def load_first_module(self):
        """Finds first available module and loads it."""
        self.load(self.find_first_module())

    def load_default_module(self):
        """Loads a module, chosen either by getting the name from TRAINED_MODEL_MODULE_NAME env var
        or from the settings file. If module file does not exist, call load_first_module()"""
        env_model_name = get_value('TRAINED_MODEL_MODULE_NAME')
        if len(env_model_name) > 3 and env_model_name[-3:] != '.py':
            env_model_name += '.py'
        if os.path.exists(os.path.join(os.path.dirname(__file__), env_model_name)):
            self.load(env_model_name)
        else:
            self.load_first_module()

    def sample(self):
        """Calls the wrapped sample() method if it exists and it's callable."""
        if self._sample is not None and callable(self._sample):
            return self._sample()
        return None

    def ready(self):
        """Calls the wrapped ready() method if it exists and it's callable. Otherwise, it figures
        out readiness by itself."""
        if self._ready is not None and callable(self._ready):
            return self._ready()
        return callable(self._init) and callable(self._run) and self.initialised

    def init(self):
        """Calls the wrapped init() method if it exists and it's callable."""
        if self._init is not None and callable(self._init):
            ret = self._init()
            self.initialised = True
            return ret
        return None

    def run(self, data):
        """Calls the wrapped run() method if it exists and it's callable."""
        if self._run is not None and callable(self._run):
            return self._run(data)
        return None

trained_model_wrapper = TrainedModelWrapper()
trained_model_wrapper.load_default_module()
