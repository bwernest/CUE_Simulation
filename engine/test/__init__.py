"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from .asserts import Assert
from .fixtures import *
from ..utils.errors import *
from ..utils.settings import Settings

# Python
import functools
import os
import shutil
from typing import Any, Callable

"""___Functions_________________________________________________________________________________"""


def void(fonction: Callable) -> Any:
    @functools.wraps(fonction)
    def fct(*args, **kwargs) -> Any:
        settings = Settings("test")
        paths = settings.paths
        if os.path.isdir(paths["folder_output"]):
            shutil.rmtree(paths["folder_output"])
        os.makedirs(paths["folder_output"])
        result = fonction(*args, **kwargs)
        shutil.rmtree(paths["folder_output"])
        os.makedirs(paths["folder_output"])
        return result
    return fct
