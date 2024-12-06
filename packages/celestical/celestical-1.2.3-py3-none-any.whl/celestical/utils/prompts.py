""" All functions that can prompt users must be here.
"""
from rich.prompt import Prompt, Confirm
from celestical.utils.display import print_help


def prompt_user(prompt: str,
                default:str=None,
                helptxt:str="",
                batch:bool=False) -> str:
    """ Prompt the user for text input.

    Parameters:
        prompt(str): the prompt text invitation
    Returns:
        str: the user input

    """
    if batch:
        return default

    more_help = ""
    if helptxt != "":
        if len(helptxt) <= 20:
            more_help = f" [gray30]({helptxt})[/gray30]"
        else:
            more_help = " [gray30](type ? for more help)[/gray30]"
    resp = Prompt.ask(f"\n [green_yellow]===[/green_yellow] {prompt}{more_help}", default=default)

    if resp is None:
        resp = ""

    if resp == "?":
        print_help(helptxt)
        return prompt_user(prompt, default, helptxt)

    return resp


def confirm_user(prompt: str, default:bool = True, batch:bool=False) -> bool:
    """ Prompt the user for yesr/no (boolean) answer.

    Parameters:
      - prompt(str): the prompt text invitation
    Returns:
      - bool: the user confirmation
    """
    if batch:
        return default

    confirmation:bool = Confirm.ask(f"\n === {prompt} ", default=default)
    if confirmation is None:
        confirmation = False
    return confirmation


def prompt_metadata_base_domain(
        default:str = ""
    ) -> str:
    """ Flow to ask for a base name

    Parameters:
      - default(str): default base domain name for an app
    """
    base_domain: str = prompt_user(
        "Indicate the base domain for your app?\n"
        +"     (e.g.  myapp.parametry.ai or parametry.ai)",
        default=default,
        helptxt="If the base domain is a subdomain, it would constitute "
            +"your base domain, e.g.: app2.celestical.net\n")
    base_domain = base_domain.strip()
    base_domain = base_domain.lower()
    if "http://" in base_domain or "https://" in base_domain:
        base_domain = base_domain.split("://")[-1]

    return base_domain

