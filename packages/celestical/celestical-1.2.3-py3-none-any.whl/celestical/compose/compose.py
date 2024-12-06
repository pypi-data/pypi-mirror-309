"""
This module contains class to manage docker compose file and their enrichment
"""
import os
import importlib.metadata
from typing import Tuple
from pathlib import Path
import yaml
import typer
import base64

from celestical.config import Config
from celestical.utils.prompts import prompt_metadata_base_domain
from celestical.utils.display import (
    print_text,
    read_wait,
    print_feedback)
from celestical.utils.prompts import (
    prompt_user,
    confirm_user)
from celestical.utils.files import extract_all_dollars


class Compose:
    """
        Class to manage docker compose file and their enrichment
    """
    def __init__(self,
            config:Config = None,
        ) -> None:
        self.config = config
        if config is None:
            self.config = Config()
        self.ecompose = {}
        self.ecompose["celestical"] = {}
        try:
            self.ecompose["celestical"]["version"] = importlib.metadata.version('celestical')
        except:
            self.ecompose["celestical"]["version"] = "O.x.y-oops"

    def set(self, key:str, value:any) -> None:
        """ Set the celestical values in self.ecompose["celestical"]
        """
        if self.ecompose is None:
            self.ecompose = {}
        if "celestical" not in self.ecompose:
            self.ecompose["celestical"] = {}
        self.ecompose["celestical"][key] = value

    def get(self, key:str) -> str:
        if self.ecompose is None:
            return ""
        if "celestical" not in self.ecompose:
            self.ecompose["celestical"] = {}
        return self.ecompose["celestical"].get(key, "")

    def services(self):
        """ Return the dictionary of services in the ecompose file
        """
        return self.ecompose.get("services", {})

    def init_ecompose(self,
            in_compose:dict = {},
            base_domain:str = "",
            domain_list:list = []) -> dict:
        """ This function initiates the enriched docker compose file
        by getting base domain name details from user.

        Parameters:
            - base_domain:str: the base domain of the app without scheme.
            - domain_list:[]: list of URLS the user already has locally and wants
              to avoid to overwrite or remake. if empty it will create
              this new app whatsoever.

        Returns:
            - the initiated enriched docker compose in dictionary format.
        """

        # --- this resets the ecompose if not empty
        if in_compose != {}:
            self.ecompose = in_compose

        # --- setting up the base_domain
        loop_n = 0
        while base_domain == "" and loop_n < 2:
            base_domain = prompt_metadata_base_domain(default=base_domain)
            loop_n += 1
            if base_domain == "" and loop_n == 1:
                print_text("We absolutely need a name for your app like:")
                print_text("\t[yellow]demo.example.org[/yellow]")
                print_text("Please type one again.")
                read_wait()

        if base_domain == "":
            print_text("Ok we will assign a random base domain for you")
            import random, string
            letters = string.ascii_lowercase
            base_domain = ''.join(
                random.choice(letters)
                for index_i in range(7))
            base_domain = base_domain + ".dev.celestical.net"
            print_text(f">>> We will use: [yellow]{base_domain}[/yellow]")

        # Checking to set base_domain only if does not exist already
        if base_domain in domain_list:
            msg = "There is already an existing app with this domain name.\n"
            msg += "Do you want to overwrite it?"
            if not confirm_user(msg):
                raise typer.Exit()

        self.set("base_domain", base_domain)
        self.set("name", base_domain)
        print_feedback(self.ecompose["celestical"]["base_domain"])
        read_wait()

        return self.ecompose

    def load_dot_env(self, env_dir:Path) -> dict:
        """ Read the .env file and extract all variables

        Returns:
            a dictionary of key value of these env variables.
        """
        env_file = env_dir / ".env"
        return self.load_env_file(env_file)

    def load_env_file(self, env_file:Path) -> dict:
        """ Read the env_file and extract all variables name and value

        Returns:
            a dictionary of key value of these env variables.
        """
        loaded_env = {}

        # - load the content of .env
        if not env_file.is_file():
            return loaded_env

        with env_file.open(mode="r") as fdesc:
            for line in fdesc:
                line = line.strip()
                if not line:
                    continue

                if line[0] == '#':
                    continue

                split_line = line.split('=', 1)
                if len(split_line) == 2:
                    k, v = split_line
                    loaded_env[k] = v
                # else line is ignored
                # .env file is supposed to define stuffs
        return loaded_env

    def _apply_os_env_or_one(self, denv:dict) -> dict:
        """ For key value dictionary where value is empty (None)
        - set the potential value from key as variable in the the OS/Shell environment
        OR
        - set it to "1" as required in the docker reference.

        None must be set prior to processing here as an empty string might be what
        a user exactly wants. None or empty value are the same when read by
        yaml.safe_load.

        Requirement all output values must be strings

        """
        for key in denv:
            if denv[key] is None:
                if key in os.environ:
                    denv[key] = os.environ[key]
                else:
                    denv[key] = "1"
        return denv

    def _separate_kvpairs(self, env:list) -> dict:
        """ For an input list of "KEY=VALUE" separate everything in a dictionary
        for accessing KEY: VALUE easily
        - if no value is found just set a the value of a KEY as an empty string

        """
        compose_env = {}

        for vardef in env:
            vardef = vardef.strip()
            varsplit = vardef.split('=', 1)
            if len(varsplit) == 2:
                compose_env[varsplit[0]] = str(varsplit[1])
            elif len(varsplit) == 1:
                compose_env[varsplit[0]] = None

        compose_env = self._apply_os_env_or_one(compose_env)

        return compose_env

    def _apply_variables(self, env:list|dict, loaded_env:dict) -> list:
        """ Read the .env file and replace all variables in the env list with their
        compose_env = {}

        Params:
            env(list): is the list of strings from environment field in
            the docker-compose file
            loaded_env: should be the content of the .env file or any default env

        Returns:
            a dictionary with all variables with their found values
            and a missing_replace parameter to tell how many variables where missed.
        """
        # - loading the content of env list of strings
        compose_env = {}

        if isinstance(env, list):
            compose_env = self._separate_kvpairs(env)
        elif isinstance(env, dict):
            # to replace names by their value in env if exist
            # else set them to one
            compose_env = self._apply_os_env_or_one(env)

        # - now applying .env (loaded_env) to compose_env
        missing_replace = 0
        for k in compose_env:
            var_str = str(compose_env[k])
            if "$" in var_str:
                # v2d var to dollars
                v2d = extract_all_dollars(var_str)
                for v in v2d:
                    missing_replace += 1
                    if v in loaded_env:
                        missing_replace -= 1
                        # replace the dollar variable
                        # with loaded_env corresponding value
                        compose_env[k] = var_str.replace(
                                            v2d[v],
                                            loaded_env[v])
                    elif v in os.environ:
                        missing_replace -= 1
                        compose_env[k] = var_str.replace(
                                            v2d[v],
                                            os.environ[v])

        # - join both env and return, update loaded with modified compose_env
        #loaded_env.update(compose_env)

        return compose_env, missing_replace

    def integrate_all_env(self, comp:dict, env_dir:Path) -> dict:
        """ Read all files from docker-compose environment and env_files and
        loads their content to re-express it in the compose environment list of
        each services.

        Returns:
            the fully integrated compose dictionary
        """
        dot_env = self.load_dot_env(env_dir)

        for key in comp.get("services", {}):
            # Variables to develop by getting them from .env and os.env
            env = comp["services"][key].get("environment", None)
            if env is not None:
                comp["services"][key]["environment"], MR = self._apply_variables(
                    env,
                    dot_env)

                print_text(f"{MR} undefined env variables in service {key}",
                    worry_level="oops")

            # environt from envfiles to add
            env_files = comp["services"][key].get("env_files", [])
            key_env = {}
            for efile in [Path(x) for x in env_files]:
                if efile.is_absolute():
                    key_env.update(self.load_env_file(efile))
                else:
                    key_env.update(self.load_env_file(env_dir / efile))

            if env is None:
                comp["services"][key]["environment"] = {}
            comp["services"][key]["environment"].update(key_env)

        return comp

    def use_built_image_names(self, compose: dict, compose_path: Path) -> dict:
        """Add the generated image name for images built in the compose file and
        remove the build definition.
        """
        base_name = compose_path.resolve().parent.name

        if "services" not in compose:
            return compose

        for service_name, service in compose["services"].items():
            if "image" not in service and "build" in service:
                service["image"] = f"{base_name}-{service_name}:latest"
                del service["build"]

        return compose

    def define_compose_path(self,
                            input_path:str) -> Path|None:
        """ Form the paths to docker-compose file and its enrichment
            according to the type of the input_path
            Note the enriched compose path is active apps ecompose path


            Returns:
                - Path of the found or guessed existing compose-file
                  or None if the input does not exist
        """
        # use current directory if nothing provided
        docker_compose_path = Path.cwd()
        file_dir = Path.cwd()

        if input_path is not None:
            if input_path != "":
                docker_compose_path = Path(input_path)

        # if input is directory we have to find the file
        if docker_compose_path.is_dir():
            file_dir = docker_compose_path
            # default most used path
            docker_compose_path = file_dir / "docker-compose.yml"

            # Order in these lists is priority, first found first selected
            base_names = ["docker-compose", "compose", "ecompose"]
            extension_names = [".yml", ".yaml"]
            for filename in \
                [base+ext for base in base_names for ext in extension_names]:
                yml_path = file_dir / filename
                if yml_path.is_file():
                    docker_compose_path = yml_path
                    break

        elif not docker_compose_path.is_file():
            # provided path does not exist
            return None

        # Finish with found file
        return docker_compose_path

    def read_docker_compose(self,
        compose_path: Path, integrate_env_files: bool=True) -> dict:
        """ Read a docker-compose.yml file.
            and integrates environment variables from files.

        Params:
            compose_path(Path): path to the docker-compose.yml file
        Returns:
            (dict): docker-compose.yml file content
                    or empty dictionary
        """
        compose = {}

        if not isinstance(compose_path, Path):
            compose_path = Path(str(compose_path))

        compose_path = compose_path.resolve()

        def logerror(message:str):
            print_text(message)
            self.config.logger.error(message)

        if compose_path.is_dir():
            logerror(f"Path is not a file: {compose_path}")
            return {}

        if compose_path.is_file():
            try:
                with compose_path.open(mode='r', encoding="utf-8") as f:
                    # Here all fields have native type
                    # integers are integers
                    compose = yaml.safe_load(f)
                    if compose is None:
                        compose = {}
            except FileNotFoundError:
                logerror(f"No file found yet at given path: {compose_path}")
                return {}
        else:
            logerror(f"No file found at given path: {compose_path}")
            return {}

        # return even if compose == {}
        return compose
                 
    def extract_secret_files(self) -> dict:
        """ Read all secrets and retrieve the path mentioned 
        from the docker compose
        """
        secrets_from_file = self.ecompose.get("secrets", {})
        all_secrets = {s_name:value.get("file")
                        for s_name, value in secrets_from_file.items()
                        if value.get("file", None) is not None}

        return all_secrets
    
    def read_top_secrets(self,
                         ecom_parent:Path,
                         ) -> dict:
        """ Read the docker secrets from the file mention and store it in
        the file
        """
        all_secrets_data = {}
        
        all_secrets = self.extract_secret_files()

        for secret, secr_path in all_secrets.items():
            file_path = Path(secr_path)
            if not file_path.is_absolute():
                file_path = (ecom_parent / secr_path).resolve()

            if not file_path.is_file():
                print("No File available Please check the path ", file_path.resolve())
                continue

            with file_path.open('rb') as secret_file:
                content = secret_file.read()
                all_secrets_data[secret] = base64.b64encode(content).decode()

                # How to decode   
                # print(
                #     base64.b64decode(
                #         bytes(all_secrets_data[secret], 'utf-8')
                #         ).decode())
                
        return all_secrets_data
    
    def integrate_top_secrets(self, ecom_parent:Path) -> bool:
        """ Save the compose secrets in celestical"""
        self.ecompose['celestical_secrets'] = self.read_top_secrets(ecom_parent)
        if self.ecompose['celestical_secrets'] == {}:
            return False

        return True