import os, os.path
import importlib
from ml_rest_api.settings import get_value

class TrainedModelWrapper(object):
    
    def __init__(self):
        self._init = None
        self._run = None
        self._sample = None
        self._ready = None
        self.initialised = False

    def load(self, module_name):
        self.module_name,_ = os.path.splitext(module_name)
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
        for filename in os.listdir(os.path.dirname(__file__)):
            if len(filename) >= 2 and filename[0:2] != '__' and filename != os.path.basename(__file__):
                module,extension = os.path.splitext(filename)
                if extension == '.py':
                    return module

    def load_first_module(self):
        self.load(self.find_first_module())

    def load_default_module(self):
        env_model_name = get_value('TRAINED_MODEL_MODULE_NAME')
        if len(env_model_name) > 3 and env_model_name[-3:] != '.py':
            env_model_name += '.py'
        if os.path.exists(os.path.join(os.path.dirname(__file__), env_model_name)):
            self.load(env_model_name)
        else:
            self.load_first_module()

    def sample(self):
        if self._sample is not None and callable(self._sample):
            return self._sample()
        else:
            return None
        
    def ready(self):
        if self._ready is not None and callable(self._ready):
            return self._ready()
        else:
            return callable(self._init) and callable(self._run) and self.initialised
        
    def init(self):
        if self._init is not None and callable(self._init):
            ret = self._init()
            self.initialised = True
            return ret
        else:
            return None
        
    def run(self, data):
        if self._run is not None and callable(self._run):
            return self._run(data)
        else:
            return None

trained_model_wrapper = TrainedModelWrapper()
trained_model_wrapper.load_default_module()
