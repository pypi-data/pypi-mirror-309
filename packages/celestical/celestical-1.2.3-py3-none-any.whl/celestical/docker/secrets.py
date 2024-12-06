"""
This module contains classes related to docker images
"""
import gzip
import shutil
from pathlib import Path
from tqdm import tqdm
from celestical.config import Config
from celestical.docker import DockerMachine
from celestical.utils.display import cli_panel, print_text, print_feedback
from celestical.utils.prompts import confirm_user
from celestical.utils.waiters import Spinner

class Image:
    """
        This class contains attributes and method to interact with a specific
        local docker image.
    """
    def __init__(self,
            config:Config = None,
        ) -> None:
        self.config = config
        if config is None:
            self.config = Config()

        self.docker = DockerMachine()
