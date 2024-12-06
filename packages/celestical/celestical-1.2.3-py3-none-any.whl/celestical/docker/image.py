"""
This module contains classes related to docker images
"""
import gzip
import shutil
from pathlib import Path
from tqdm import tqdm
from celestical.config import Config
from celestical.utils.files import get_most_recent_file
from celestical.docker import DockerMachine
from celestical.utils.display import print_text
from celestical.utils.prompts import confirm_user

class Image:
    """
        This class contains attributes and method to interact with a specific
        local docker image.
    """
    def __init__(self,
            config:Config = None,
        ) -> None:
        self.config = config
        if config is None:
            self.config = Config()

        self.docker = DockerMachine()

    def confirm_zip_path(self,
            image_name: str,
            project_name: str,
            gz_paths: list) -> (Path, Path):
        """Confirms with user whether to rezip or not if image zip file exists and updates
           gz_paths accordingly
        Params:
            images: string or list of strings of image full tag names
                    as they should appear in the "image" field of each service
            project_name: a string given to name the project, usually the base
                    domain name
            gz_paths: A list of path to gzipped images to be uploaded
        Returns:
            zipfile path
        """
        # --- preparing save directory
        save_path = Path(f"/tmp/celestical/{project_name}/")
        # Create the save_path directory and any necessary parent directories
        save_path.mkdir(parents=True, exist_ok=True)

        # --- preparing list of images, or of 1 image
        escaped_image_name = image_name.replace('/', '__')
        escaped_image_name = escaped_image_name.replace(':', '_-_')
        gz_filename = save_path / f'{escaped_image_name}.tar.gz'
        gz_filename_local = Path(f'{escaped_image_name}.tar.gz')

        if not gz_filename_local.is_file():
            gz_filename_local = None

        return gz_filename, gz_filename_local

    def compress_images(self, images: str|list[str], project_name: str) -> list[Path]:
        """Compress one or several Docker images. Checking if compressed file
        does not already exist.

        Params:
            images: string or list of strings of image full tag names
                    as they should appear in the "image" field of each service
            project_name: a string given to name the project, usually the base
                    domain name
        Returns:
            A list of path to gzipped images to be uploaded
        """
        image_names = []
        gz_paths = []

        # --- Getting docker client
        client = self.docker.get_docker_client()
        if client is None:
            self.config.logger.debug("Docker client could not be found.")
            return gz_paths

        # --- preparing list of images, or of 1 image
        if isinstance(images, str):
            image_names = [images]
        else:
            image_names = images

        # --- Compressing all images in different gzips
        for image_name in image_names:

            gz_filename, cwd_gz_filename = self.confirm_zip_path(image_name, project_name, gz_paths)
            if cwd_gz_filename is not None:
                gz_filename = get_most_recent_file(gz_filename, cwd_gz_filename)

            if gz_filename.exists():
                if not confirm_user(
                    f"[yellow]{image_name}[/yellow] already prepared,"
                    +f"\n\trenew and overwrite {gz_filename} ?",
                    default=False):
                    # Using existing compressed file
                    print_text(f" * Ok, using ready file: {gz_filename}\n")
                    gz_paths.append(gz_filename)
                    continue

            # Step 1: Calculate the total size of the image
            # for chunk in client.images.get(image).save(named=True):
            #     tar_file.write(chunk)
            print_text(f"Working on {image_name}...")
            img = None
            try:
                self.config.logger.debug("Using docker client to image.get: %s", image_name)
                img = client.images.get(image_name)
            except Exception as oops:
                self.config.logger.debug(oops)
                img = None

            if img is None:

                # --- try with calling command line
                ### docker save image_name | gzip > gz_filename
                #if cmd is not None:
                #    gz_paths.append(gz_filename)
                #    print_text(f"[green]succesfully prepared[/green]: {gz_filename}")
                #    continue

                # else
                msg = (
                    f"Image {image_name} not found for project: {project_name}. If "
                    "this image is built in the compose file, please run "
                    "'docker compose build' first."
                )
                print_text(msg,
                        worry_level="ohno")
                self.config.logger.debug(msg)
                continue

            # --- Get the tar image and calculate its size
            self.config.logger.debug("Checking Image Size: %s", img)
            image_data = img.save(named=True)
            total_size = sum(len(chunk) for chunk in image_data)
            total_size_mb = total_size / (1024 * 1024)

            print_text(f"Image Tag Found: {image_name}"
                    +f"\n\timage size: {total_size_mb:.2f} MB"
                    +f"\n\tsaving in: {gz_filename.resolve().parents[0]}"
                    +f"\n\tas file name: {gz_filename}")

            # --- Reset the image data iterator for creating the tar archive
            image_data = img.save(named=True)

            # Save the Docker image to a gzip file with a progress bar
            print_text(f"Exporting compressed image (gzip) to {gz_filename} ...")
            with gzip.open(gz_filename, 'wb') as gz_file:
                with tqdm(total=total_size,
                        unit='B',
                        unit_scale=True,
                        desc="exporting") as pbar:
                    # Read, compress, and write data in chunks
                    for chunk in image_data:
                        gz_file.write(chunk)
                        pbar.update(len(chunk))

            gz_paths.append(gz_filename)
            print_text(f"[green]succesfully prepared[/green]: {gz_filename}")

        return gz_paths
