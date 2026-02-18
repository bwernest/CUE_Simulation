"""___Modules___________________________________________________________________________________"""

# CUE_Simulation
from ..utils.settings import Settings

# Python
import os
import shutil
from typing import Callable

"""___Functions_________________________________________________________________________________"""


def void(fonction: Callable) -> any:
    def fct(*args, **kwargs) -> any:
        settings = Settings("test")
        paths = settings.paths
        if os.path.isdir(paths["folder_data"]):
            shutil.rmtree(paths["folder_data"])
        os.makedirs(paths["folder_data"])
        result = fonction(*args, **kwargs)
        shutil.rmtree(paths["folder_data"])
        os.makedirs(paths["folder_data"])
        return result
    return fct
