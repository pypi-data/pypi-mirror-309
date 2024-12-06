"""
This module contains classes related to interaction with local docker engine.
"""
from pathlib import Path
import shutil
from prettytable import PrettyTable, ALL
import docker
from docker.types import SecretReference, EndpointSpec
from docker.models.services import Service
from docker.models.containers import Container
from docker.models.secrets import Secret
import time

from celestical.config import Config

class DockerMachine:
    """
    This class contains attributes and method to interact with local docker engine. 
    """

    DEFAULT_SECRET_PATH = "/run/secrets/"
    
    def __init__(self, config:Config = None):
        self.config = config
        if config is None:
            self.config = Config()
        self.client = self.get_docker_client()

    def _build_unix_socket(self, socket_path: Path) -> str:
        return 'unix://' + str(socket_path.resolve())

    def _connect_docker_colima(self) -> docker.DockerClient:
        """ Try to establish client connection with colima
        """
        current_ctx = docker.context.Context.load_context(
            docker.context.api.get_current_context_name())
        if current_ctx is None:
            return None
        url = current_ctx.endpoints["docker"]["Host"]
        return docker.DockerClient(base_url=url)

    def get_docker_client(self):
        """ Returns a docker client taken from local environment """
        client = None
        try:
            self.config.logger.debug("Searching docker API client from_env()")
            client = docker.from_env()
        except Exception as oops:
            err_msg = "Could not connect to the docker service. Is it really running?"
            self.config.logger.debug(err_msg)
            self.config.logger.error(oops)
            client = None

        # alternative to finding docker
        if client is None:
            try:
                self.config.logger.debug("Searching docker API from system socket.")
                client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
            except Exception as oops:
                self.config.logger.error(oops)
                client = None

        if client is None:
            try:
                self.config.logger.debug("Searching docker API from userspace socket.")
                user_tilde = Path("~")
                user_home = user_tilde.expanduser()
                socket_path = user_home / ".docker/run/docker.sock"
                client = docker.DockerClient(base_url=self._build_unix_socket(socket_path))
            except Exception as oops:
                self.config.logger.error(oops)
                client = None

        # alternative to finding docker on Mac or Linux running Colima
        if client is None:
            try:
                self.config.logger.debug("Searching docker API client via context (Colima)")
                client = self._connect_docker_colima()
            except Exception as oops:
                self.config.logger.error(oops)
                client = None

        #if client is None:
        # then use call to command line docker client
        return client

    def get_ports(self,
              image_id:str,
              proto:str="tcp") -> str:
        """ Get ports from containers created from the specified image.
            else get the ExposedPorts info from the image itself.

            Params:
                image_id(str): should the string hash of the image
                docker_clienti(any): a docker client
                proto(str): (unused for now) ports for a that specific protocol,
                by default 'tcp'
            Returns:
                a string for a joint list of ports
        """
        if self.client is None:
            # We retry again in case it is a timing issue
            self.client = self.get_docker_client()
            if self.client is None:
                # Do nothing or do it via command lines
                return ""
            # else continue

        ports = set()

        # Checking from containers
        for container in self.client.containers.list(all=True):
            if container.image.id == image_id:
                port_data = container.attrs['HostConfig']['PortBindings']
                if port_data:
                    for port, bindings in port_data.items():
                        # get only the port number, not the protocol
                        ports.add(str(port.split('/')[0]))

        # Checking from listed images
        if len(ports) == 0:
            try:
                img = self.client.images.get(image_id)
                for tcpport in [str(attr).split("/")[0]
                                for attr in
                                img.attrs["Config"]["ExposedPorts"]
                                if "tcp" in attr]:
                    ports.add(tcpport)
            except Exception as oops:
                # The image_id is not found
                # The ports set remains empty and that's all ok.
                self.config.logger.debug(oops)

        return ",".join(sorted(ports))

    def list_local_images(self) -> PrettyTable|None:
        """List all docker images locally available with port information.

        Returns:
            PrettyTable of formatted table of docker images
        """
        if self.client is None:
            # We retry again in case it is a timing issue
            self.client = self.get_docker_client()
            if self.client is None:
                # Do nothing or do it via command lines
                return None

        table = PrettyTable()
        table.field_names = ["Image ID", "Image Name", "Tags", "Ports"]
        table.hrules = ALL  # Add horizontal rules between rows

        images = []
        terminal_width = 100
        try:
            terminal_width, _ = shutil.get_terminal_size()
            images = self.client.images.list()
        except Exception as whathappened:
            self.config.logger.error(whathappened)
            return table

        # Adjust column widths based on the terminal width
        # divide by 2 for two lines
        id_width = max(len(image.id) for image in images) // 2 + 1
        name_width = max(len(image.tags[0].split(':')[0])
                        if image.tags
                        else 0 for image in images)
        # divide by 2 to leave space for the Ports column
        tags_width = (terminal_width - id_width - name_width - 7) // 2
        ports_width = tags_width
        table.align["Image ID"] = "l"
        table.align["Image Name"] = "l"
        table.align["Tags"] = "l"
        table.align["Ports"] = "l"
        table._max_width = {
            "Image ID": id_width,
            "Image Name": name_width,
            "Tags": tags_width,
            "Ports": ports_width}

        for image in images:
            # Split the Image ID into two lines
            half_length = len(image.id) # // 2
            formatted_id = f'{image.id[:half_length]}\n{image.id[half_length:]}'
            # Extract image name from the tags
            image_name = image.tags[0].split(':')[0] if image.tags else 'N/A'
            # Get ports
            ports = self.get_ports(image.id)
            table.add_row([formatted_id, image_name, ', '.join(image.tags), ports])

        return table

    def get_docker_secrets(self) -> list[Secret]:
        """ Retrieve all the docker secretes from the machine """
        try:
            secrets = self.client.secrets.list()
        except docker.errors.APIError as oops:
            print(f"Error fetching secrets: {oops}")
            return []

        return secrets

    def get_docker_secret_with_name(self, secret_name:str) -> Secret|None:
        """ Retrieve a docker secretes from the machine with
        the given secret_id 
        """
        if secret_name is None:
            return {}

        try:
            secret = self.client.secrets.get(secret_name)
        except docker.errors.APIError as oops:
            print(f"Error fetching secrets: {oops}")
            return None

        return secret

    def create_secret_references_from_secrets(self, all_secrets:list) -> list:
        """ Creates the SecretReferences to create the services"""
        if all_secrets is None:
            return []

        secrets_references = [SecretReference(secret.id, secret.name)
                              for secret in all_secrets]
        return secrets_references

    def get_all_services(self) -> list:
        """ Get all the available service names """
        all_service_names = [each.name for each in self.client.services.list()]
        if len(all_service_names) == 0:
            return []

        return all_service_names

    def get_service_with_service_name(self, service_name:str) -> Service|None:
        """ Get service by the service_name given """
        service = self.client.services.get(service_name)
        if service is None:
            return None

        return service

    def remove_services_with_name(self, service_name:str) -> bool:
        """ Delete the service with the name given """
        service = self.get_service_with_service_name(service_name)
        if service is None:
            return False

        try: 
            service.remove()
        except Exception as oops:
            print("Error occurred while deleted the services as ", oops)
            return False

        return True
    
    def create_endpoint_spec(self, 
                             internal_port:int = 8080,
                             external_port:int = 3040):
        """ Create EndpointSpec with internal port and external given"""
        return EndpointSpec(mode="vip",
                            ports={external_port:
                                   internal_port})

    def create_service(self, 
                       secrets,
                       endpoint_spec: EndpointSpec,
                       name:str = "default_service", 
                       image:str = "nginx:alpine-slim"
                       ) -> Service|None:
        """ Create a service with given secrets, endpoint_spec
        name and image_name return true on the success
        """
        if secrets is None:
            print("Creating the service without the service")

        if (len(secrets) >= 1 ) \
              and (not isinstance(secrets[0], SecretReference)):
            print("Please send the right format of secrets")
            return None

        if endpoint_spec is None:
            print("Creating service without the port information")

        if (endpoint_spec is not None ) \
            and not isinstance(endpoint_spec, EndpointSpec):
            print("Please send the right format of Endpoints")
            return False

        try:
            service = self.client.services.create(
                        image=image,
                        name=name,
                        secrets=secrets,
                        endpoint_spec=endpoint_spec
                        )
        except Exception as oops:
            print("Error occurred while creating service as ", oops)
            return None

        return service

    def filter_containers_by_name(self, name:str) -> list:
        """ Filtered Containers by the given name"""
        filtered_containers = self.client.containers.list(
                                    filters={"name": name})

        if len(filtered_containers) == 0:
            return []

        return filtered_containers

    def exec_retrieve_secrets(self,
                              secret_files:list,
                              container_id:str,
                              ) -> dict:
        """ Retrieve Secrets from the secret files inside the container
          and store it in a dictionary"""
        secret_contents = {}

        if len(secret_files) == 0:
            return secret_contents

        for secret_file in secret_files:
            try:
                cmd_read_secret = r'cat /run/secrets/' + secret_file
                exec_result_read = self.client.api.exec_create(
                    container=container_id, cmd=cmd_read_secret
                )
                secret_content = self.client.api.\
                            exec_start(exec_result_read.get("Id"))

                secret_contents[secret_file] = secret_content.decode('utf-8')

            except Exception as oops:
                print(f"Error reading file {secret_file} as {oops}")
                secret_content[secret_file] = 'Failed'

        return secret_contents

    def create_list_of_secrets_in_container(self,
                                            container_id:str,
                                            ) -> list:
        """ A list of secrets from the default Folder inside the
        docker container
        """
        cmd_list_secrets = "ls -1 " +  self.DEFAULT_SECRET_PATH

        exec_result = self.client.api.exec_create(
                        container=container_id, cmd=cmd_list_secrets
                        )
        secret_list_output = self.client.api.exec_start(
                                exec_result.get("Id", ""))

        secret_files = secret_list_output.decode('utf-8').splitlines()

        return secret_files
    
    def retrieve_secrets_from_docker_container(self,
                                               secrets_names:list,
                                               service_name:str 
                                                 = "service_celestical",
                                               image:str = "nginx:alpine-slim",
                                               external_port:int = 8908
                                               ) -> dict:
        all_secrets = self.get_docker_secrets()
        # Validate the docker secrets
        all_secret_names = [secrets.name for secrets in all_secrets]
        available_secrets_names = list(set(all_secret_names).\
                                       intersection(secrets_names))
        if len(available_secrets_names) == 0:
            print("No secrets available with that name")
            return {}

        all_secrets = [self.get_docker_secret_with_name(each) 
                       for each in available_secrets_names]
        
        references_secrets = self.create_secret_references_from_secrets(
                                        all_secrets)
        
        endpoint_spec = self.create_endpoint_spec(external_port=external_port)
        
        server_info = self.create_service(
                        name=service_name,
                        image=image,
                        secrets=references_secrets,
                        endpoint_spec=endpoint_spec
                        )
        if server_info is None:
            print("service not created successfully")
            return {}
        
        # To start the container
        time.sleep(6)
        
        container = self.filter_containers_by_name(server_info.name)
        if len(container) != 1:
            print("Error occurred hence there are multiple or no container with the"+
                "same name")
            return {}

        all_secrets_in_container = self.create_list_of_secrets_in_container(container[0].id)
        if len(all_secrets_in_container) == 0:
            print("No secrets inside the container")
            return {}

        secret_information = self.exec_retrieve_secrets(
                            all_secrets_in_container,
                            container_id=container[0].id
                            )
            
        self.remove_services_with_name(service_name)
        
        # A dictionary with the secret name and its values
        return secret_information
