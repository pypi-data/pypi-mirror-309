"""
This module contains classes related to select command of celestical CLI tool
"""
import typer
from rich.console import Console
from celestical.app.app import App
from celestical.commands.app import AppCommand
from celestical.utils.display import cli_panel, prompt_user


class Select:
    """
    This class consist of attributes and methods to select the active app
    (finalize and set the active_app_id).
    """

    def __init__(self) -> None:
        self.app = App()
        self.cli_app = AppCommand()
        self.console = Console()
