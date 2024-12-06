""" user related class

    This file holds the routines to login, register
    and manage user data and configuration.
"""
import getpass
from typing import Tuple
import importlib.metadata

from celestical.api import (
    ApiClient,
    ApiException,
    AuthApi,
    UtilsApi,
    UserCreate,
    Configuration)
from celestical.api.exceptions import UnauthorizedException

from celestical.config.config import Config
from celestical.utils.display import cli_panel, print_text
from celestical.utils.prompts import confirm_user, prompt_user

class User:
    """
    A class used to represent user.
    """
    def __init__(self, config:Config = None) -> None:
        self.current_celestical_version = importlib.metadata.version('celestical')
        self.config = config
        if config is None:
            self.config = Config()

        # All user config
        self.user_data = None

    @property
    def username(self):
        """Property getter for the username
        """
        if self.user_data is None:
            return ""
        return self.user_data.get("username", "")

    def to_rich(self) -> str:
        """Text to is play in rich format
        """
        msg = ">>> "
        if self.is_logged_in():
            msg += f"You are logged in as [yellow]{self.username}[/yellow]"
        else:
            msg += "You are not logged in"
        return msg

    def _register_form(self, ask:str = "Register with or without a [b]special code[/b]",
        default_code:str = ""
        ) -> str:
        """The registration form which ask user the special code"""
        if ask != "":
            print_text(ask)
        user_code = prompt_user("[b]special code[/b] (optional)", default=default_code)
        return user_code

    def _login_form(self,
            ask:str = "Please enter your [i]celestical[/i] credentials",
            default_email:str = None
            ) -> Tuple[str, str]:
        """ The username/password form to login and register """

        if ask != "":
            print_text(ask)

        # -------------- username
        user_mail = prompt_user("work email", default=default_email)
        if "@" not in user_mail:
            self.config.logger.error("Entered email address is missing a '@'")
            cli_panel(message="Email is incorrect: no @ sign found.", kind="error")
            return self._login_form(ask)

        # -------------- password
        password = getpass.getpass(" *** password: ")
        self.config.logger.info("Password succesfully created.")

        if len(password) == 0:
            self.config.logger.error("Password was empty")
            cli_panel(message="Password was empty!", kind="error")
            return self._login_form(ask="Please re-enter your [i]celestical[/i] credentials")

        if len(password) <= 7:
            self.config.logger.error("Password is too short - less than 8 chars")
            cli_panel(message="Password too short - less than 8 chars!", kind="error")
            return self._login_form(ask="Please re-enter your [i]celestical[/i] credentials")

        return (user_mail, password)

    def user_login(self,
            default_email:str = None,
            force_relog:bool = False,
            ) -> bool:
        """ Login to Celestical Cloud Services via the CLI.

        Returns:
            bool
        """
        self.config.logger.info("Entering user login function in user.py")
        if self.user_data is None:
            self.user_data = self.config.load_config()

        if default_email is not None:
            self.user_data['username'] = default_email

        prask = ""

        if force_relog:
            if not self.config.reset_config():
                return False

            # self.user_data was loaded before the reset
            if "username" in self.user_data:
                if self.user_data['username'] is None or self.user_data['username'] == "":
                    return self.user_login(default_email=None)
                # else we've got a previous email info
                return self.user_login(default_email=self.user_data['username'])

            return self.user_login()

        # From this point we have not been in force_relog condition
        if len(self.user_data["access_token"]) > 10 and  len(self.user_data["username"]) > 3:
            default_email = self.user_data["username"]
            prask = f"Previously logged in as [yellow][i]{default_email}[/i][/yellow]"


        if prask != "":
            (username, password) = self._login_form(ask=prask, default_email=default_email)
        else:
            (username, password) = self._login_form(default_email=default_email)

        apiconf = self.config.api_configuration()
        with ApiClient(apiconf) as api_client:
            # Create an instance of the API class
            api_instance = AuthApi(api_client)

            save_ok = False
            try:
                # Auth:Jwt.Login
                api_response = api_instance.auth_jwt_login_auth_jwt_login_post(username, password)
                self.config.logger.debug("We did get a login api response")
                if api_response.token_type != "bearer":
                    self.config.logger.debug("This client does not handle"+
                                                 " non bearer type token")
                    return False

                if len(api_response.access_token) < 10:
                    self.config.logger.debug("Received token seems invalid")
                    return False

                # Collect all user data and save it
                self.config.logger.debug("Creating and saving user data/conf.")
                data = {
                    "created": self.config.celestical_date(),
                    "username": username,
                    "access_token": api_response.access_token,
                    "token_type": api_response.token_type
                }
                save_ok = self.config.save_config(data)
            except ApiException as api_exp:
                self.config.logger.error("Code Enceladus: ApiException when "+
                                             "logging in. Assuming wrong user,password tuple.")
                self.config.logger.debug(api_exp)
                print_text("Sorry user/password are not matching. Not logged in",
                        worry_level="ohno")
                return False
            except Exception as oops:
                self.config.logger.error("Code Mars: could not connect, try"+
                                             " again after checking your connection.")
                self.config.logger.debug(oops)
                print_text("Sorry we could not log you in, please try again.",
                        worry_level="ohno")
                return False

        return save_ok

    def user_register(self) -> int:
        """Register as a user for Celestical Cloud Services via the CLI."""

        user_code = self._register_form()

        (user_mail, password) = self._login_form("")
        repassword = getpass.getpass(" *** re-enter password: ")
        flag = 0

        if repassword != password:
            msg = "Re-entered password does not match. "
            msg += 'Please run [blue]celestical register[/blue] again to register'
            print_text(text=msg, worry_level="ohno")
            flag += 2
            return flag

        apiconf = self.config.api_configuration()

        with ApiClient(apiconf) as api_client:
            auth = AuthApi(api_client=api_client)

            apires = None
            try:
                apires = auth.register_register_auth_register_post(
                        user_create=UserCreate(
                            email=user_mail,
                            password=password,
                            code=user_code
                            )
                        )
            except ApiException as api_err:
                msg = f"---- Registration error ({api_err.status})"
                self.config.logger.error(msg)
                self.config.logger.debug(apires)
                if api_err.body:
                    self.config.logger.debug(api_err.body)
                else:
                    self.config.logger.debug(api_err.reason)
                return flag
            except Exception as oops:
                self.config.logger.error(oops)
                return flag
        config = self.config.load_config()
        current_user = "" if config['username'] == '' \
                        else f"from [yellow]{config['username']}[/yellow]"
        msg = 'Do you want to switch your default user '
        msg += f"{current_user} to [yellow]{user_mail}[/yellow]"
        flag += 1
        cli_panel('You have successfully registered')
        if config["username"] == '' or confirm_user(msg):
            config["username"] = user_mail
            flag += 1
            if self.config.save_config(config):
                flag += 1

        return flag

    def load_user_creds(self, _apiconf:Configuration) -> Tuple[bool, str]:
        """ Reads user creds from config and set access token

            _apiconf from api.Configuration() in api_configuration()
            is set with latest access token.
        """
        user_data = self.config.load_config()

        if user_data is not None and isinstance(user_data, dict):
            # cover the case of an apiKey type security
            _apiconf.api_key['Authorization'] = \
            user_data.get("access_token", "")
            _apiconf.api_key_prefix['Authorization'] = \
            user_data.get("token_type", "bearer")
            # cover the case of an http+bearer type security
            # (this is current default on celestical's API side
            _apiconf.access_token = user_data.get("access_token", "")
            return True, "Loaded creds for API request"

        msg = "[red] You need to login or relogin before proceeding[/red]\n"
        msg += ">>> [underline]celestical login[/underline]"
        return False, msg

    def get_api_with_auth(self) -> Configuration|None:
        """
             This function returns configured api if the token is valid.
             Else it returns None.

            Returns:
                - A configured api.Configuration object.
        """
        apiconf = self.config.api_configuration()
        setcred, mesg = self.load_user_creds(apiconf)
        if setcred is False:
            cli_panel(mesg)
            return None
        return apiconf

    def is_logged_in(self) -> bool:
        """
        Gets the login status of user from the config file.
        Returns a string containing the login status
        """
        # forcing reload
        self.user_data = self.config.load_config()

        if not (self.user_data is None
                or self.user_data == {}):
            # else message that config cannot be loaded will be shown.
            tok = self.user_data.get("access_token", "")
            username = self.user_data.get("username", "")

            # Clear nope
            if tok == "":
                return False

            # Else we've got to check with server
            if username != "":
                apiconf = self.get_api_with_auth()
                if apiconf is None:
                    return False

                api_response = None
                with ApiClient(apiconf) as api_client:
                    utils_api = UtilsApi(api_client)
                    try:
                        self.config.logger.debug("Testing token endpoint")
                        api_response = utils_api.test_token_exists_uuwe_get_with_http_info()
                    except UnauthorizedException as oops:
                        self.config.logger.debug(oops)
                        return False
                    except Exception as oops:
                        self.config.logger.debug(oops)
                        return False

                if api_response.status_code == 200:
                    return True

        return False


    def welcome(self, verbose:int=2) -> str:
        """ Return a global welcome message

            verbose from 0 (short) to 2 (long)
        """
        wcol = "purple"
        welcome_message:str = f"[{wcol}]Direct deployment of containers or compose" \
                            +" files to an independent green cloud made by space" \
                            +f" engineers[/{wcol}] " \
                            +f"(version: {self.current_celestical_version})\n\n"

        if verbose > 0:
            if self.is_logged_in():
                welcome_message += \
                    f"\n - Current user: [{wcol}]{self.username}[/{wcol}]"
            else:
                welcome_message += "\n - No signed in user"

        if verbose > 1:
            welcome_message += "\n\n [underline]Usual workflow steps[/underline]" \
                            +"\n\t [1] (only once) Register with command " \
                            +f"[{wcol}]celestical register[/{wcol}]" \
                            +"\n\t [2] Login with command " \
                            +f"[{wcol}]celestical login[/{wcol}]" \
                            +"\n\t [3] Deploy with command " \
                            +f"[{wcol}]celestical deploy[/{wcol}]\n\n"

        return welcome_message
