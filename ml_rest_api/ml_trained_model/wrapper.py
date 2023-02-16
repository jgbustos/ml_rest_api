"""This module implements the TrainedModelWrapper class."""
import os
import os.path
import importlib
from threading import Thread
from types import ModuleType
from typing import Optional, Iterable, Callable, Dict
from ml_rest_api.settings import get_value

WrapperCallableType = Optional[Callable]


class TrainedModelWrapper:
    """TrainedModelWrapper class acts as adapter for programmatically chosen ML trained model
    module. The init(), run() and sample() methods call the module's identically named methods.
    """

    def __init__(self) -> None:
        """Initialise everything to None, particularly init, run, sample and ready methods."""
        self._init: WrapperCallableType = None
        self._run: WrapperCallableType = None
        self._sample: WrapperCallableType = None
        self.initialised: bool = False
        self.module_name: Optional[str] = None
        self.module: Optional[ModuleType] = None

    def load(self, module_name: str) -> None:
        """Loads a Python module, binding the init, run and sample callable methods."""

        def find_callable(callable_name: str) -> WrapperCallableType:
            """Returns a named attibute if it exists and it's callable"""
            if hasattr(self.module, callable_name):
                funct = getattr(self.module, callable_name)
                if callable(funct):
                    return funct
            return None

        self.module_name, _ = os.path.splitext(module_name)
        self.module = importlib.import_module(
            "ml_rest_api.ml_trained_model." + self.module_name
        )
        self._init = find_callable("init")
        self._run = find_callable("run")
        self._sample = find_callable("sample")

    @staticmethod
    def find_first_module() -> str:
        """Finds first available module (the first Python module found in the current dir that is
        not this wrapper or starts with __). Returns the name minus .py extension"""
        for filename in os.listdir(os.path.dirname(__file__)):
            if len(filename) < 2:
                continue  # too short a filename
            if filename[0:2] == "__":
                continue  # ignore __init__,py and similar
            if filename == os.path.basename(__file__):
                continue  # ignore this very module
            module, extension = os.path.splitext(filename)
            if extension == ".py":
                return module
        return ""

    def load_default_module(self) -> None:
        """Loads a module, chosen either by getting the name from TRAINED_MODEL_MODULE_NAME env var
        or from the settings file. If module is not found in env var or settings, find it by calling
        load_first_module()"""
        env_model_name: str = get_value("TRAINED_MODEL_MODULE_NAME")
        if not env_model_name:
            env_model_name = self.find_first_module()
        if env_model_name:
            self.load(env_model_name)

    def ready(self) -> bool:
        """Returns whether the model was initialised and a wrapped run() method can be called"""
        return bool(self._run) and self.initialised

    def multithreaded_init(self) -> None:
        """Calls self.init() to load the model in a separate thread."""
        if self._init:
            Thread(target=self.init).start()

    def init(self) -> None:
        """Calls the wrapped init() method if it's assigned."""
        if self._init and not self.initialised:
            self._init()
            self.initialised = True

    def run(self, data: Iterable) -> Dict:
        """Calls the wrapped run() method if it's assigned."""
        if self._run:
            return self._run(data)
        return {}

    def sample(self) -> Dict:
        """Calls the wrapped sample() method if it's assigned."""
        if self._sample:
            return self._sample()
        return {}


trained_model_wrapper = TrainedModelWrapper()  # pylint: disable=invalid-name
trained_model_wrapper.load_default_module()
