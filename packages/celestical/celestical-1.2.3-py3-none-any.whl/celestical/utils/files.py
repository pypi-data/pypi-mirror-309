import logging
import string
import yaml
from pathlib import Path
import json

from celestical.utils.display import (
    print_text,
    print_console
    )

def save_json(data: dict,
        batch:bool=False,
        cli_logger:logging.Logger=None) -> bool:
    """Helper function to save the complete stack info.
    Params:
        data(dict): complete info about the stack (name, compose ..)
    Returns:

    """
    if "name" not in data:
        return False

    json_file = f'stack_{data["name"]}.json'
    try:
        with open(json_file, 'w') as jfile:
            json.dump(data, jfile, indent=4)
    except Exception as oops:
        if not batch:
            print_text(f"Error: JSON file could not be saved f'stack_{data['name']}.json'")
        if cli_logger is not None:
            cli_logger.debug(oops)
        return False

    return True


def save_yaml(
        data: dict,
        yml_file:Path = None,
        batch:bool = False,
        cli_logger:logging.Logger = None) -> Path|None:
    """Helper function to save the complete stack info.
    Params:
        data(dict): complete info about the stack (name, compose ..)
        yml_file(Path):  Path where to save the file
    Returns:

    """
    #yml_file = "docker-compose.yml"
    if yml_file is None:
        yml_file = Path("./.docker-compose-enriched.yml")

    try:
        with yml_file.open(mode='w') as yfile:
            yaml.dump(data, yfile, default_flow_style=False)
        if not batch:
            print_text(f"YAML file created successfully: [green]{yml_file}[/green]")

    except Exception as eoops:
        msg = f'Error: Unable to save data to {yml_file}'
        if cli_logger is not None:
            cli_logger.error(msg)
            cli_logger.error(eoops)
        return None

    # return the Path object of the saved file
    return yml_file


def get_most_recent_file(file1:Path,
                         file2:Path) -> Path:
    """ Will compare modification time between file1 and file2
        and return most recent one.
        If no file exist

    Params:
        - file1(str): file Path
        - file2(str): file Path
    """
    # --- cover cases if one or both are null
    if file1 is None:
        if file2 is None:
            return None
        else:
            return file2
    elif file2 is None:
        return file1
        # else keep going

    # --- select last modified or file1
    selected_path = file1
    ftime1 = 1.0
    if file1.is_file():
        ftime1 = file1.stat().st_mtime

    ftime2 = 0.0
    if file2.is_file():
        ftime2 = file2.stat().st_mtime

    if ftime2 > ftime1:
        selected_path = file2

    return selected_path


def extract_all_dollars(str_in:str) -> dict:
    """ Extract all dollar variables names from the string

    Returns:
        A dictionary that has  pure variable names as keys
        as they would be found defined in an shell env or .env file
        and they representation in strings as $variables or ${variables}.

    """
    # - split the strings and manage where to start
    splits = str_in.strip() # we dont need whitespaces

    if len(splits) <= 1:
        # we need at least 2 characters to work out at least one $variable
        return {}

    s_idx = 1
    if splits[0] == '$':
        # use first split, so start at index 0
        s_idx = 0

    splits = str_in.split("$")
    if len(splits) <= 1:
        return {}

    used_vars = {}
    accepted_chars = string.ascii_letters + string.digits + "_"
    # - each split start with a variable or '{'
    for spp in splits[s_idx:]:
        var = ""
        if len(spp) > 1:
            if spp[0] == '{':
                # get all up to next first '}'
                idx = spp.find('}')
                if idx > 1:
                    var = spp[1:idx]
                    used_vars[var] = "${"+var+"}"
                # else not adding the var.
            else:
                for char in spp:
                    if char in accepted_chars:
                        var += char
                    else:
                        # stop at first unaccepted char
                        break
                if len(var) >= 1:
                    used_vars[var] = "$"+var

    return used_vars
