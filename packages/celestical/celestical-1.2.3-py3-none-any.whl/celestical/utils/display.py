"""Helper display functions for the celestical app"""
import typer
import time

from prettytable import PrettyTable, ALL
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

READ_DELAY = 0.8

# For each service type there is a list of keywords to detect them
SERVICE_TYPES = {
    "FRONTEND": ["web", "www", "frontend", "traefik",
                 "haproxy", "apache", "nginx"],
    "API": ["api", "backend", "service", "node"],
    "DB": ["database", "redis", "mongo", "mariadb", "postgre"],
    "BATCH": ["process", "hidden", "compute"],
    "OTHER": []
}


def read_wait():
    """ Cognitively we might have to wait for the readers
    """
    time.sleep(READ_DELAY)


# Building a table in the terminal
def create_empty_table(columns_labels):
    """Create an empty table with specified columns."""
    pt = PrettyTable()

    # Set the field names (columns)
    pt.field_names = columns_labels

    return pt


def add_row_to_table(table:PrettyTable, row_dict):
    """Add a row to the table based on a dictionary."""
    if set(row_dict.keys()) != set(table.field_names):
        raise ValueError("Row dictionary keys do not match table columns.")
    table.add_row([row_dict[col] for col in table.field_names])


def cli_create_table(data: dict) -> Table:
    """Create a table from a dictionary.
    Params:
        data(dict): dictionary to be displayed
    Returns:
        (Table): table object
    """
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Key", style="dim")
    table.add_column("Value")

    for key, value in data.items():
        table.add_row(str(key), str(value))

    return table


def write_app_row(
        app:dict,
        key:int=0,
        active_app_id:str="",
        indent_space:str="") -> str:
    """ Common representation of an app in a list

    Parameters:
      - indent_space: white spaces or other things to start lines
      - active_app_id: the string of the current active app_id
        which is externally defined from here.
      - key: which number this entry should have appearing
      - app: dictionnary to define an app, expecting fields like id,
        created_date, url
    """
    app_id = app.get("id", "-")
    active = "[r]ON[/r]" if active_app_id == app_id else "  "
    acolor = "yellow" if active_app_id == app_id else "grey50"
    app_id_str = "[grey42]"+app_id+"[/grey42]"

    app_url = app.get("url", "")
    if app_url == "":
        app_url = "[ no domain ]"

    cdate = app.get('created_date', "no-date")
    cdate_s = cdate.split("T")
    if len(cdate_s) > 1:
        cdate = f"[grey42]{cdate_s[0]}[/grey42]"
        cdate += f" [grey54]{cdate_s[1]}[/grey54]"

    one_app_row  = f"\n{indent_space} {active} "
    one_app_row += f"> {key}/ [{acolor}]{app_url}[/{acolor}]"
    one_app_row += f"\n{indent_space}      ({cdate}) {app_id_str}"

    return one_app_row


def cli_panel(
        message: str,
        title:str="Celestical - Current Step",
        kind="info",
        batch:bool=False) -> None:
    """Display a message in a panel.
    Params:
        message(str): message to be displayed
    Returns:
        None
    """

    if batch:
        return

    # Note: here is hwo to join *args
    # buffer = "\n".join(str(arg) for arg in args)

    if kind == "info":
        title = title
        panel = Panel(message, title=f"[bold purple]{title}[/bold purple]",
                    border_style="purple",
                    expand=True,
                    title_align='left')
    elif kind == "error":
        title = "Celestical CLI Error"
        panel = Panel(message, title=f"[bold red]{title}[/bold red]",
            border_style="red",
            expand=True,
            title_align='left')

    console.print(panel)


def print_nested_dict(dictionary: dict, batch:bool=False):
    """Print a nested dictionary in a readable format."""
    if batch:
        return
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print_nested_dict(value)
        else:
            print(f"{key}: {value}")


def print_feedback(used_input:str, batch:bool=False):
    """ Show users what they have input """
    if batch:
        return
    console.print(f" :heavy_check_mark: - {used_input}")


def print_help(help_text: str, batch:bool=False):
    """ Show users a help text """
    if batch:
        return
    console.print(" [dodger_blue3]<:information:>[/dodger_blue3] "
                +f"[gray30]{help_text}[/gray30]")


def print_console(msg: str):
    """Simple console print"""
    console.print(msg)
    read_wait()


def print_text(text: str, worry_level="chill"):
    """Print text to the CLI.

    Parameters:
      - text(str): the text to print
      - worry_level(str): a level of worries that would change the color;
        chill, oops, ohno
    Returns:
      - str: the text to print
    """
    msg = f"{text}"
    if worry_level == "oops":
        msg = f"[orange]{text}[/orange]"
    elif worry_level == "ohno":
        msg = f"[red]{text}[/red]"

    # add prefix
    msg = " --- " + msg

    return console.print(msg)


def guess_service_type_by_name(service_name: str, img_name:str=""):
    """ Quick guess of service type
    """

    if len(service_name) == 0:
        return ""

    service_name = service_name.lower()

    for stype in SERVICE_TYPES:
        for guesser in SERVICE_TYPES[stype]:
            if guesser in service_name:
                return stype

    if img_name != "":
        img_name = img_name.lower()
        for stype in SERVICE_TYPES:
            for guesser in SERVICE_TYPES[stype]:
                if guesser in img_name:
                    return stype

    # if nothing found
    return "OTHER"


def dict_to_list_env(d_in:dict) -> list:
    env_list = []
    for key in d_in:
        env_list.append(key+"="+str(d_in[key]))
    return env_list

