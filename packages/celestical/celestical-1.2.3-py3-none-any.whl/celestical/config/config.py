"""
Managing the local configuration for the Celestical services
"""
import json
import os
import logging
import datetime
from pathlib import Path
from celestical import api

class Config:
    """
    A class used to represent application configration
    """

    # Defining the host is optional and defaults to http://localhost
    # See configuration.py for a list of all supported configuration parameters.
    API_SCHEME = "https"
    API_HOST = "moon.celestical.net"
    API_URL = API_SCHEME + "://" + API_HOST

    # LOGGING_LEVEL = logging.DEBUG
    # logging.basicConfig(encoding='utf-8', level=LOGGING_LEVEL)

    HOTLINE = "starship@celestical.net"
    PRODUCTION = True
    BATCH_MODE = False

    def __init__(
            self,
            verify_ssl = True,
            host: str = "",
            scheme: str = "") -> None:
        """ Initialize the configuration object

        Parameters:
            - verify_ssl: will be used to verify the ssl connection when making
              Celestical API connections. Only cases where users are behind
              proxies that rewrites the SSL certificates would that be
              necessary (large companies, or local antivirus)
            - host: a custom host to connect to. must contain the port if
              relevant.
            - scheme: a custom scheme to use, it must be http or https.
        """
        if len(host) > 3:
            self.API_HOST = host
        if len(scheme) > 3:
            self.API_SCHEME = scheme
        self.API_URL = self.API_SCHEME + "://" + self.API_HOST

        self.cli_setup()
        # Creation of the CLI-wide logger -> celestical.log
        self.logger = self.create_logger(production=self.PRODUCTION)
        self.verify_ssl = verify_ssl

    def api_configuration(self) -> api.Configuration:
        """
        Configures the api for making requests.

        Returns:
            api.Configuration typed api configuration
        """
        conf_for_api = api.Configuration(host=self.API_URL)
        conf_for_api.verify_ssl = self.verify_ssl
        #conf_for_api.assert_hostname = True
        conf_for_api.tls_server_name = self.API_HOST

        return conf_for_api

    def get_batch_mode(self) -> bool:
        """
        Gets the batch mode attribute of the config class.

        Returns:
            Bool typed batch mode
        """
        return self.BATCH_MODE

    def celestical_date(self) -> str:
        """
        Returns current datetime in predefined format as a string.

        Returns:
            Path typed path to the directory containing config json file
        """
        return str(datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%S'))

    # Service types definitions
    def get_default_config_dir(self) -> Path:
        """
        Returns the default directory path of config file as Path instance

        Returns:
            Path typed path to the directory containing config json file
        """
        path = Path.home() / ".config" / "celestical"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_app_config_dir(self) -> Path:
        """
        Returns the default app directory path of app files(like ecompose file)
        as Path instance.

        Returns:
            - Path typed path to the directory containing app files
        """
        path = self.get_default_config_dir() / "apps"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def get_default_config_path(self) -> Path:
        """Return the default config path for this application

        Returns:
            Path typed path to the config json file
        """
        path = self.get_default_config_dir() / "config.json"
        return path

    def get_active_app_id_path(self) -> Path:
        """ Gets the path to the file that holds the active App ID
        """
        path = self.get_app_config_dir() / "active_app_id"
        return path

    def get_default_log_path(self) -> Path:
        """Return the default log file path for this application

        Returns:
            Path typed path to the log file
        """
        path = self.get_default_config_dir() / "celestical.log"
        return path

    def _get_default_config_data(self) -> dict:
        data = {
            "created": self.celestical_date(),
            "username": "",
            "access_token": "",
            "token_type": "",
            "batch": False
        }
        return data

    def reset_config(self) -> bool:
        """ 
        Reset config is used to logout and start login protocol from scratch

        Returns:
            Bool typed confirmation weather reseted config is saved or not
        """
        # Similar to a logout: forgetting token
        data = {
            "created": self.celestical_date(),
            "username": "",
            "access_token": "",
            "token_type": "",
            "batch": False
        }
        return self.save_config(data)

    def load_config(self, config_path: str = "") -> dict:
        """Load config file from config_path.

        Params:
            config_path(str): non-default absolute path of the configuration.
        Returns:
            (dict): configuration content
        """
        path = self.get_default_config_path()
        if config_path is not None and config_path != "":
            path = Path(config_path)

        user_data = {}
        if path.exists():
            try:
                with open(path, 'r',encoding='utf-8') as f_desc:
                    user_data = json.load(f_desc)
            except Exception :
                # Use only standard print function
                print(" *** could not read the celestical configuration file.")
                user_data = {}

        default_data = self._get_default_config_data()
        for key in default_data:
            if key not in user_data:
                user_data[key] = default_data[key]

        return user_data

    def save_config(self, config:dict) -> bool:
        """Save config file to the default_config_path.

        Params:
            config(dict): configuration.
        Returns:
            (bool): True if saving process went fine
        """
        cpath = self.get_default_config_path()

        try:
            if not cpath.parent.exists():
                os.makedirs(cpath.parent, exist_ok=True)
        except Exception as oops:
            self.logger.debug("save_config: directory couldn't be created.")
            self.logger.debug(oops)
            return False

        # Check if all fields are saved for uniformization
        if "created" not in config:
            config["created"] = self.celestical_date()
        if "username" not in config:
            config["username"] = ""
        if "access_token" not in config:
            config["access_token"] = ""
        if "token_type" not in config:
            config["token_type"] = ""
        if "batch" not in config:
            config["batch"] = False

        try:
            with cpath.open(mode='w') as fdescr:
                json.dump(config, fdescr, indent=4)
        except Exception as oops:
            self.logger.debug("save_config: config file couldn't be written.")
            self.logger.debug(oops)
            return False

        return True

    def cli_setup(self) -> bool:
        """ Setup necessary directories.
        """
        config_path = self.get_default_config_dir()
        try:
            config_path.mkdir(parents=True, exist_ok=True)
        except Exception :
            return False
        return True

    def create_logger(self, production: bool=False) -> logging.Logger :
        """A function to create and configure the logger for the Celestical CLI
        Params:
            production(bool): if False, set log level to debug
        Returns:
            (logger): the logger object
        """
        log_format = "%(asctime)s --%(levelname)s: %(message)s"
        log_location = self.get_default_log_path()

        logging.basicConfig(
            encoding='utf-8',
            filename=log_location,
            format=log_format,
            filemode="a",
            level=logging.WARNING if production else logging.DEBUG,
        )
        logger = logging.getLogger(name="Celestical CLI")
        if production is False:
            logger.debug("Starting Logger in DEBUG Mode: %s", log_location)
        else:
            logger.warning("Starting Logger in WARNING Mode: %s", log_location)
        return logger

    def get_active_app(self) -> str:
        """
        This function return the path to directory containing active app ecompose file.

        Returns:
            - active app id as a string if no app is active returns None.
        """
        path = self.get_active_app_id_path()
        active_app = ""
        try:
            if path.exists():
                active_app = path.read_text()
        except Exception as oops:
            self.logger.warning("Could not read current active app id, continuing.")
            self.logger.warning(oops)
            active_app = ""

        return active_app

    def delete_active_file(self, selected_app_id: str = "_") -> bool:
        """ Delete text file about the active app
        information
        
        If selected_app_id is empty it forces to delete the file
        """
        if selected_app_id != self.get_active_app():
            return False

        active_file_path = self.get_active_app_id_path()
        if not active_file_path.exists():
            msg = "File not found while delete the "
            msg += "active app file"
            self.logger.warning(msg)
            return False

        # Delete the active file
        try:
            active_file_path.unlink()
        except Exception as oops:
            msg = "Issue: Could not delete the active file"
            self.logger.warning(msg)
            self.logger.warning(oops)
            return False

        return True
