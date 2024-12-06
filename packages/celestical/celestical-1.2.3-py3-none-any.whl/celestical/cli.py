"""The CLI to interface with the Celestical Serverless Cloud."""
from typing import Optional
import typer
from typing_extensions import Annotated

from celestical.utils.display import cli_panel, print_console, print_text
from celestical.config import Config
from celestical.session import Session
from celestical.utils.prompts import confirm_user
from celestical.user import User
#from celestical.commands.select import Select
# Prepare is Enrich+etc
#from celestical.commands.prepare import Prepare
from celestical.docker.image import Image
from celestical.docker.docker import DockerMachine
from celestical.app.app import App

user = User()
user.config.logger.info("Starting CLI.")

app = typer.Typer(pretty_exceptions_short=False,
                  no_args_is_help=True,
                  help=user.welcome(),
                  rich_markup_mode="rich")


# @app.callback(invoke_without_command=True)
@app.command()
def apps(delete_app_id: str =
             typer.Option(
                 None,
                 "--delete",
                 "-d",
                 help="Delete an application by the app id"),
         force_delete: bool =
             typer.Option(
                 False,
                 "--force",
                 "-f",
                 help="Delete the apps without any prompt"),
                 ):
    """ List all apps from current user."""
    session = Session(needs_login=True)
    # If delete mode  
    # session.delete_app(delete_app_id, force=force_delete, )
    
    # Else display the apps for beginner and inform the actions of
    # delete/select active an app
    session.app_actions()

#     print(dir(session))
#     if delete_app_id and force_delete: 
#         docker_app = App(delete_app_id)
#         app_status = docker_app.delete_app()
#         print_console(app_status)
#         return app_status

#     if delete_app_id:
#         confirm_delete = confirm_user(
#         f"Would you like to delete the App {delete_app_id}? [y/n] (n): ",
#         default=False)
#         if confirm_delete:
#             docker_app = App(delete_app_id)
#             app_status = docker_app.delete_app()
#             print_console(app_status)
#             return app_status
#         return None


#     app_table, _ = session.get_apps_table()
#     print_console(app_table)
#     change_active = confirm_user(
#         "Would you like to set or change the active app?",
#         default=False)
    
#     print_console(
#         """ If you tend to delete apps you could use --delete-app or -d flag with apps
#  Example:
#      celestical apps -d [appid]
#                 or
#      celestical apps --delete-app [appid]""")
#     print(delete_app_id)
    
    

    # print("Hooray")



@app.command()
def login() -> None:
    """Login to Celestical Cloud Services via the CLI.
        The session is explicitly set to force relogin.
    """
    session = Session(needs_login=True, force_login=True)
    if session.user is not None:
        print_console(session.user.to_rich())


@app.command()
def register():
    """Register as a user for Celestical Cloud Services via the CLI."""
    flag = user.user_register()
    config = user.config.load_config()
    if flag == 0:
        print_text("User already exists or We could not connect.")
    if flag in (1,3):
        mgs = "You can now login with user "
        mgs += f"[yellow]{config['username']}[/yellow] using [blue]celestical login[/blue]"
        cli_panel(mgs)


@app.command()
def images():
    """ List all local docker images for you.
        Similar to 'docker image ls'.
    """
    docker_machine = DockerMachine()
    table = docker_machine.list_local_images()

    if table is None:
        cli_panel("Docker service is [red]unaccessible[/red]\n")
    else:
        cli_panel("The following are your local docker images\n"
                 +f"{table}")


@app.command()
def deploy(compose_path: Optional[str] =
             typer.Argument(
                 default="./",
                 help="Path(str) to compose file. Default current directory"),
           verify_ssl: Optional[bool] =
             typer.Option(
                 default=True,
                 help="Default will verify TLS/SSL certificates. False to " \
                 + "help you manage cases when behind firewalls."),
           api_host: Optional[str] =
             typer.Option(
                 default="",
                 help="Custom host (including port) for API connections. " \
                 + "Mostly used for testing."),
           api_scheme: Optional[str] =
             typer.Option(
                 default="",
                 help="Custom connection scheme; http or https. " \
                 + "Mostly used for testing.")):
    """ Select, prepare and push your applications (docker-compose.yml) to the
    Celestical Cloud.

        1. Deploying means necessity to connect, so creating connected Session
        2. Select the application or create a new one
        3. Check if enrichment is necessary
            3.1. enrich
        4. Push ecompose images (todo check which image to push)
    """
    config = None
    if len(api_host) > 3 or len(api_scheme) > 3:
        config = Config(host=api_host, scheme=api_scheme)

    session = Session(needs_login=True, config=config)

    if session.select_app() is True:
        # Enrich using the input compose file
        if session.app.enrich(compose_path):
            # Push (and deploy) the necessary images
            session.app.push()


@app.command()
def prepare(compose_path: Optional[str] =
            typer.Argument(
                default="./",
                help ="Path(str) to compose file. Default current directory")):
    """
    Prepare the enriched compose file for the given application.

    """
    #session = Session()
    #session.select_app(app_id)

    #prepare = Prepare()
    #prepare.prepare(compose_path)


@app.command()
def push(app_id:Optional[str]=
         typer.Argument(
            default=None,
            help = "App Id(str) you wish to push to Celestical cloud")):
    """
    Pushes the application to celestical cloud.
    """
    # TODO adapt with new code
    user_app = App()

    # if app_id is None:
    #     enriched_compose = app.read_app_ecompose(user_app.get_active_app())
    # else:
    #     select(app_id)
    #     enriched_compose = app.read_app_ecompose(user_app.get_active_app())

    # if enriched_compose is None:
    #     msg = "To continue with deployment you need a celestical account.\n"
    #     msg += "see command: [yellow]celestical register[/yellow]"
    #     cli_panel(msg)
    #     raise typer.Exit()

    # if enriched_compose == {}:
    #     msg = "The ecompose file is not proper.\n"
    #     msg += "Please prepare the enriched compose file for the given App"
    #     cli_panel(msg)
    #     prepare()

    # image = Image()
    # image.upload_images(app_uuid=enriched_compose["celestical"]["app_id"],
    #                     e_compose=enriched_compose)


# ----- only for testing docker secrets
#@app.command()
#def docker_secrets(
#        compose_path: Optional[str] =
#             typer.Argument(
#                 default="./",
#                 help="Path(str) to compose file. Default current directory"),
#        all_secrets: Optional[str] =
#            typer.Argument(
#                default=["file"],
#                help="The docker secrets which to converted")
#    ):
#    """ Docker secrets retrieval """
#    if compose_path:
#        crypt_symmentric = CryptSymmetric(secret_key=SECRET_KEY, 
#                                           init_vector=INIT_VECTOR,
#                                           encrypt_bytes=128)
#        encrypted_data = crypt_symmentric.encrypt_docker_compose_secrets(
#                                            compose_path)
#        print(encrypted_data)
#
#        return encrypted_data
#
#    docker = DockerMachine()
#    try:
#        docker_value = docker.retrieve_secrets_from_docker_container(
#                            service_name="radom",
#                            secrets_names=[all_secrets],
#                            external_port=8080
#                            )
#        
#        print_text(docker_value)
#    except Exception as oops:
#        msg = f"Error occurred while retrieving the secrets as {oops}"
#        print_text(msg)
#    
