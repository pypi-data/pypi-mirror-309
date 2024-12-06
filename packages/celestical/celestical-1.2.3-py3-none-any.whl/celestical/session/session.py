"""
This module contains classes related to app command of celestical CLI tool
"""
from typing import Tuple
import typer
from pathlib import Path

from celestical.api.exceptions import UnauthorizedException
from celestical import api

from celestical.app import App
from celestical.user import User
from celestical.config.config import Config
from celestical.utils.display import (
    print_text, write_app_row,
    print_console, cli_panel, 
    print_feedback)
from celestical.utils.prompts import prompt_user

class Session:
    """
    // former AppCommand
    This class consist of attributes and methods to select the active app
    (finalize and set the active_app_id).
    """

    def __init__(
            self,
            needs_login: bool = False,
            force_login: bool = False,
            config: Config | None = None,
            batch_mode: bool = False,
            select_app: bool = False) -> None:
        """Initialize a session with a user and a selected app

            Parameters:
                - needs_login: boolean to indicate if the user needs to be
                  logged in. In case true and if user does not have a valid
                  token, the prompt will ask to login again
                - config: potential injectable config objects, especially
                  interesting to configure TUI wide batch mode
                - batch_mode: boolean to activate batch processing if True.
                  Default is False to have user interactions.
                - select_app: boolean to force app selection if True.
                  Default is False so that session object can be a placeholder
        """
        self.app = None
        self.user = None

        self.config = config
        if config is None:
            self.config = Config()

        if force_login is True or needs_login is True:
            # if so want to make sure user is logged in then and be able to call
            # that from anywhere.
            self.user = self.get_logged_in_user()
            if self.user is None:
                raise typer.Abort()

        if force_login is True and self.user is not None:
            self.user.user_login(force_relog=True)

        # By default the session object does nothing else
        # specific actions can be then called
        if select_app is True:
            self.select_app()

    def get_logged_in_user(self) -> User:
        """

          1- Loads local user credentials
          2- If token is not empty -> check auth with token
          3- If no token or invalid token -> login
          4- If token is ok continue.

        """
        user = User(config=self.config)
        if not user.is_logged_in():
            if user.user_login():
                return user
            return None

        return user

    def _retrieve_app_index_from_id(self,
                                       apps: dict,
                                       app_id: str) -> list:
        """ Retrieve the all the similar app id from the app information given

        Parameters:
            - apps: A dictionary of the app information
            - app_id: given id from the user

        Returns:
            - list: apps index
        """
        selected_app_index = [index for index, app in apps.items()
                              if (app.get("id", "_").startswith(app_id)) or
                              (app.get("id", "_").endswith(app_id))]
        return selected_app_index

    def _retrieve_app_index_from_index(self,
                                       apps: dict,
                                       user_index: str) -> list[str]:
        """ Search the all the similar app index from the app information given

        Parameters:
            - apps: A dictionary of the app information
            - app_id: given id from the user

        Returns:
            - list: apps index
        """
        selected_app_index = [key for key in apps
                              if user_index == key]
        return selected_app_index

    def _retrieve_app_index_from_url(self, apps: dict, url: str) -> list[str]:
        """ Select all the index which has the url given

        Parameters:
            - apps: a dictionary of all the apps information
            - url: a str to select the app

        Returns:
            - list: apps index
        """
        selected_app_ids = [index for index, app in apps.items() if url in app["url"]]
        return selected_app_ids

    def get_apps_table(self, start_index: int = 1) -> Tuple[str, dict]:
        """Create a table string with all apps (from API)
           marking the active app for user to select
        """
        apps = self.get_apps_list()

        if apps is None:
            return "", None

        active_app_id = self.config.get_active_app()

        # --- arrange list for remote apps
        cli_table = "\n>>>> Your Celestical Apps"
        if len(apps) == 0:
            cli_table = "\n>>>> You have no Celestical Apps, yet! :-) "
            cli_table += "\n     use:  [b]celestical deploy[/b] [i]my-docker-compose.yml[/i]"
        
        for key, app in apps.items():
            # Filtering app info
            one_app_row = write_app_row(app, key, active_app_id)
            cli_table += one_app_row

        # --- arrange list for local apps
        #     for these with ID not in remote apps
        local_apps = self.get_local_apps_list(
            rapps=apps,
            start_index=len(apps)+1)
        if len(local_apps) == 0:
            # we are done here and return normal result
            return cli_table, apps

        # Local apps formatting
        cli_table = "\n\n>>>> Your Local Apps, not pushed yet"
        for key, app in local_apps.items():
            one_app_row = write_app_row(app, key, active_app_id)
            cli_table += one_app_row

        return cli_table, apps

    def get_local_apps_list(
            self,
            rapps: dict,
            start_index: int = 1) -> dict:
        """Get local apps in folder that are not part of remote listing

            rapps: should be a mapping between a string based index
            and an app object (dict)
        """
        app_dir = self.config.get_app_config_dir()
        app_listing = {}

        key = start_index
        for app in app_dir.iterdir():
            if app.is_dir():
                app_id = str(app.name)
                if app_id not in [rapps[p].get("id", ":")
                                  for p in rapps]:
                    app_listing[key] = {"id": app_id}
                    key += 1
        return app_listing

    def get_apps_list(
            self,
            call_nbr: int = 1,
            start_index: int = 1) -> dict:
        """ Get the list of apps for given user from celestical cloud.

            Returns:
                - list of api.models.app.App
                  or an empty list of user could not be logged in.
        """
        if self.user is None:
            return {}

        apiconf = self.user.get_api_with_auth()
        if apiconf is None:
            return {}

        api_response = None
        with api.ApiClient(apiconf) as api_client:
            app_api = api.AppApi(api_client)

            try:
                api_response = app_api.get_user_apps_app_get()

            except UnauthorizedException as oops:
                self.config.logger.debug(oops)

                # In case we try too many times we are out
                if call_nbr > 1:
                    msg = "[red]Access not authorized for now[/red]\n\n"
                    msg += "Make sure a payment method is installed\n"
                    msg += "If problem persists please contact us: "
                    msg += f"{self.config.HOTLINE}"
                    cli_panel(msg)
                    raise typer.Exit()

                # Let's try to relog again as last resort
                if call_nbr <= 1 and not self.user.user_login():
                    if not self.user.user_login(force_relog=True):
                        print_text(
                            "Please start over again; "
                            + "Re-enter your credentials carefully.",
                            worry_level="ohno")
                        raise typer.Exit()

                call_nbr += 1
                self.config.logger.debug(oops)
                return self.get_apps_list(call_nbr)
            except Exception as oops:
                self.config.logger.debug(oops)
                cli_panel("Could not connect; check your connection.")
                raise typer.Exit()

        res = api_response
        if isinstance(api_response, api.models.app.App):
            res = [api_response]

        dres = {}
        app_nb = start_index
        for item in res:
            dres[str(app_nb)] = item
            app_nb += 1

        return dres

    def select_app(
            self,
            app_id: str = "") -> bool:
        """ This method sets active App ID with given App ID.

        If no App ID is given checks with user and makes them choose from a
        list of existing apps or create new app.

        Else we just inform which app was activated. Still showing the table.

        Parameters:
            - app_id:str: App ID to select and to be set as active app.


        """
        # active_app = self.get_active_app()
        cli_table, apps = self.get_apps_table()
        msg = ""

        # Direct active APP setup with an app_id input
        if len(app_id) >= 3:

            selected_app_ids = self._retrieve_app_index_from_id(apps, app_id)

            if len(selected_app_ids) == 1:
                # Nominal case
                self.app = App(
                    app_id=selected_app_ids[0],
                    user=self.user)
                self.app.set_as_active_app()
                return True
            # elif len(selected_app_ids) == 2 or more:
            #   continue
            msg = "[bold]The App ID provided does not exist[/bold]\n"

        # From here we need a selection process if apps is not empty
        if len(apps) == 0:
            # No aps to select from so Creating a new app
            self.app = None
            msg += ">>> Creating a new app for you."
            print_console(msg)
            # This creates an App from scratch
            self.app = App(user=self.user)
            self.app.set_as_active_app()
            msg = "Setting your new app as the active App.\n"
            msg += str(self.app)
            cli_panel(message=msg, title="New App Created")
            return True

        # ------- User has to chose which app to activate
        cli_panel(
            message=cli_table,
            title="Select one of your Apps")

        # Ask question to select an app
        app_id = self._select_from_list(apps)

        # if app_id is empty this corresponds to creating an app
        url_list = [apps[app_a].get("url", "_")
                    for app_a in apps]
        self.app = App(
            app_id=app_id,
            user=self.user,
            domain_list=url_list)

        self.app.set_as_active_app()
        return True

    def _select_from_list(self, apps: list) -> str:
        """ This method asks user to choose an app ID or index (int)

        if the user provided option exactly total number of app +1
        redirects to create new app.  unless t

        Parameters:
          - apps:list of app object (api.models.app.App)

        Returns:
          - uuid of the app selected by user
        """
        active_app = self.config.get_active_app()

        # Asking for an input
        msg = "Select the app number to work on, or N for a new one"
        if active_app is None:
            active_app = ""

        if active_app != "":
            msg = "Enter to continue with active app, or choose another app"

        active_app_key = ""
        for app_d in apps:
            if apps[app_d].get("id", "") == active_app:
                active_app_key = app_d

        app_num_str = prompt_user(
            prompt=msg,
            default=active_app_key,
            helptxt="Choose an App number or 'N' to create a new one")

        # Reacting to user input
        #  No input == continue with active or new if no input
        #  'N' or anything is meaning to create a new app
        app_num = 0
        if app_num_str == "":
            if active_app != "":
                return active_app
            # setting up app_num for new app creation
            app_num = len(apps)+1

        if app_num == 0:
            try:
                app_num = int(app_num_str)
            except ValueError:
                app_num = len(apps)+1

        if (app_num_str not in apps) or (app_num >= len(apps)+1):
            msg = ""
            if app_num_str.lower() not in ["n", "new", "neu"]:
                msg += f"\nI know [b]{app_num_str}[/b] does not look like"
                msg += " a 'N' or 'new', I'll go with it anyway\n"
            msg += "Few questions and deployment will be done."
            msg += "\n\nSo let's create your new App!"
            cli_panel(msg, title="Creating a new app")
            return ""

        # Return ID of selected App
        app_id = apps.get(app_num_str, {}).get("id", "")
        return app_id

    def _select_apps_from_app_choice(self,
                                     app_list: dict,
                                     app_choice: str) -> list[str]:
        """ Select the app index assuming choice as url, index and id

        Parameters:
            - apps: A dictionary of the app information
            - app_choice: given response from the user

        Returns:
        """
        selected_apps_keys = []
        selected_app_index_by_index = self._retrieve_app_index_from_index(
                                                app_list,
                                                app_choice)
        selected_apps_keys.extend(selected_app_index_by_index)

        selected_app_index_by_id = []
        selected_app_index_by_url = []
        if len(app_choice) >= 3:
            selected_app_index_by_id = self._retrieve_app_index_from_id(
                                                app_list,
                                                app_choice)
            selected_app_index_by_url = self._retrieve_app_index_from_url(
                                                    app_list,
                                                    app_choice)
            selected_apps_keys.extend(selected_app_index_by_id)
            selected_apps_keys.extend(selected_app_index_by_url)
        sorted_list = sorted(list(set(selected_apps_keys)))
        return sorted_list
    
    def delete_app(self, app_list: dict) -> bool:
        """ Action to delete the app """
        prompt_delete_app = "Which app do you want to [red]delete[/red]?"
        app_choice = prompt_user(prompt=prompt_delete_app)
        if len(app_choice) == 0:
            print_text("Nothing selected.")
            return False

        # --- Get app id
        app_id = ""
        chosen_apps_keys = self._select_apps_from_app_choice(
                                    app_list,
                                    app_choice)
        # if len(app_choice) == 1 and app_choice.isdigit():

        if len(chosen_apps_keys) == 1:
            # On obvious choice
            app_id = app_list[chosen_apps_keys[0]]["id"]

        elif len(chosen_apps_keys) > 1:
            # several choices
            # list the apps ask for the other choice
            print_text("Several choices are possible")

        else:
            # Ask the user to choose an app
            print_text("No app found for your choice")

        if app_id == "":
            return False

        self.config.delete_active_file()

        if self.app is not None and self.app.app_id == app_id:
            self.app.delete_app()
            return True

        app = App(app_id)
        app.delete_app()
        return True

    def app_actions(self) -> bool:
        """ All th possible actions for the apps by the user
        """
        apps_table, app_list  = self.get_apps_table()

        if app_list == {}:
            return False

        msg = "Actions:\n"
        msg += "    1/ Activate an app (a)\n"
        msg += "    2/ [red]Delete[/red] an app (d)"

        cli_panel(apps_table, title="Apps")
        print_text(msg)
        user_action_choice = prompt_user("Select an action", default="")
        user_action_choice = user_action_choice.lower()

        # if user_action_choice == "a":
        #     prompt_active_app = "Would you like to set or change the active app?"

        #     user_action_choice = prompt_user(prompt=prompt_active_app)
        #     if user_action_choice:
        #         if self.select_app(user_action_choice):
        #             print('hello')
        #     return None
        # # print("Work on the activate apps")

        if user_action_choice in ["d", "del", "delete", "2"]:
            return self.delete_app(app_list)

        print_text("Nothing done")
        return False