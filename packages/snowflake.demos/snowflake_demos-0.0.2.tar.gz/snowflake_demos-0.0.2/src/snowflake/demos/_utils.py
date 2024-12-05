import csv
import io
import logging
import os
import shutil
import urllib
import zipfile

from typing import Dict, Optional, Tuple

import requests

from cachetools import Cache, cached
from rich.table import Table

from snowflake.core import CreateMode, Root
from snowflake.core.notebook import Notebook
from snowflake.demos._constants import (
    DATA_DIR,
    DEMO_DATABASE_NAME,
    DEMO_MAPPING_COLUMN_WIDTHS,
    DEMO_MAPPING_COLUMNS,
    DEMO_MAPPING_FILE_PATH,
    DEMO_REPO_URL_COLUMN,
    DEMO_SCHEMA_NAME,
    DEMO_STAGE_NAME,
    DEMO_WAREHOUSE_NAME,
    ENVIRONMENT_FILE_PATH,
    NOTEBOOK_DIR,
)
from snowflake.demos._demo_connection import DemoConnection
from snowflake.demos._environment_detection import CONSOLE_MANGAER


logger = logging.getLogger(__name__)

check_repo_exists = os.path.isdir


def find_notebook_file(step: int, directory: str) -> Optional[str]:
    """Find a file with the given number followed by an underscore and a name containing alphabets and underscores.

    Parameters
    __________
      number: The number to search for.
      directory: The directory to search in.

    Returns
    _______
      The file name if found, otherwise None.
    """
    if not os.path.exists(directory):
        return None
    for file in os.listdir(directory):
        if file.startswith(str(step) + "_"):
            return file
    return None


@cached(Cache(maxsize=10))
def get_repo_name_from_url(url: str) -> Optional[str]:
    """Extract the repository name from a Git URL.

    Parameters
    __________
      url: The URL of the Git repository.

    Returns
    _______
      The repository name, or None if the URL is invalid.
    """
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path.strip("/")
    components = path.split("/")
    if len(components) >= 2:
        return components[-1] + "-main"
    return None


def download_repo(repo_url: str, repo_name: str, demo_name: str, refresh_data: bool = False) -> bool:
    """Download the repository from the given URL.

    Parameters
    __________
      repo_url: The URL of the repository.
      refresh_data: If True, the repository will be downloaded even if it already exists.
    """
    logger.info(f"Downloading repository from {repo_url}")
    zip_url = repo_url + "/archive/refs/heads/main.zip"

    # we will create a data directory in the current directory
    # and clone the repository into it
    data_dir = os.path.join(os.path.dirname(__file__), DATA_DIR)
    os.makedirs(data_dir, exist_ok=True)

    if check_repo_exists(os.path.join(data_dir, repo_name)) and not refresh_data:
        logger.debug(f"Repository {repo_name} already exists. Skipping download.")
        return True

    CONSOLE_MANGAER.safe_print(f"Downloading repository {repo_url} ...", color="yellow", end="")
    response = requests.get(zip_url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall(data_dir)
        CONSOLE_MANGAER.safe_print("✅", color="green", bold=True)
    else:
        CONSOLE_MANGAER.safe_print("❌", color="red", bold=True)
        CONSOLE_MANGAER.safe_print("Failed to download the repository", color="red")
        CONSOLE_MANGAER.safe_print(
            f"Please check your internet connection and reload the demo using load_demo('{demo_name}', refresh_demo=True).",  # noqa: E501
            color="red",
        )
        return False
    return True


# In-memory caching
def read_demo_mapping_with_cache() -> Dict[str, Dict[str, str]]:
    """Read the demo mapping CSV file and cache the data in memory.

    Returns
    _______
      The demo mapping data as a dictionary.
    """
    # Read the CSV file
    demo_file_path = os.path.join(os.path.dirname(__file__), DEMO_MAPPING_FILE_PATH)
    demo_map: Dict[str, Dict[str, str]] = {}
    if not hasattr(read_demo_mapping_with_cache, "cached_data"):
        with open(demo_file_path) as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                demo_name = row[0]
                demo_info = {header[i]: row[i] for i in range(1, len(header))}
                demo_map[demo_name] = demo_info
            read_demo_mapping_with_cache.cached_data = demo_map  # type: ignore[attr-defined]
    return read_demo_mapping_with_cache.cached_data  # type: ignore[attr-defined]


def get_url_from_demo_name(demo_name: str) -> str:
    """Get the URL of the demo repository from the demo name.

    Parameters
    __________
      demo_name: The name of the demo.

    Returns
    _______
      The URL of the demo repository.
    """
    demo_mapping = read_demo_mapping_with_cache()
    return demo_mapping[demo_name][DEMO_REPO_URL_COLUMN]


def get_notebook_name_from_file_name(file_name: str, demo_name: str) -> str:
    """Get the notebook name from the file name.

    Parameters
    __________
      file_name: The name of the notebook file.

    Returns
    _______
      The name of the notebook.
    """
    return demo_name.replace("-", "_") + "_" + file_name[2:-6]


def print_demo_list() -> None:
    """Print the list of available demos."""
    demos = read_demo_mapping_with_cache()

    CONSOLE_MANGAER.safe_print("List of Examples:", color="cyan")

    table = Table(
        show_header=True,
        header_style="bold magenta",
        safe_box=True,  # Use ASCII characters for borders
        expand=False,  # Don't expand to terminal width if not needed
        show_lines=True,  # This adds lines between rows for better readability
    )

    # Add columns
    for i in range(len(DEMO_MAPPING_COLUMNS)):
        table.add_column(
            DEMO_MAPPING_COLUMNS[i],
            max_width=DEMO_MAPPING_COLUMN_WIDTHS[i],
            overflow="fold",
            style="blue",
        )

    # Add rows
    for demo_name, demo_info in demos.items():
        table.add_row(
            *[
                demo_name,
                demo_info[DEMO_MAPPING_COLUMNS[1]],
                demo_info[DEMO_MAPPING_COLUMNS[2]],
                demo_info[DEMO_MAPPING_COLUMNS[3]],
            ]
        )

    CONSOLE_MANGAER.print_table(table)


def create_demo_notebooks(demo_name: str, repo_name: str, num_steps: int, root: Root) -> bool:
    """Create a default notebook for the given demo.

    Parameters
    __________
      demo_name: The name of the demo.
      notebook_path: The path to save the notebook.
      root: The root connection to Snowflake.
    """
    logger.info(f"Creating demo notebooks for {demo_name}")

    stage_handle = root.databases[DEMO_DATABASE_NAME].schemas[DEMO_SCHEMA_NAME].stages[DEMO_STAGE_NAME]

    demo_directory = get_demo_directory(demo_name)
    notebook_file_directory = os.path.join(demo_directory, NOTEBOOK_DIR)

    environment_file_path = os.path.join(demo_directory, ENVIRONMENT_FILE_PATH)
    CONSOLE_MANGAER.safe_print(
        f"[yellow]Uploading files to stage[/yellow] "
        f"[green]{DEMO_STAGE_NAME}/{repo_name}[/green] [yellow]and creating notebooks...[/yellow]",
        color="yellow",
    )
    if os.path.exists(environment_file_path):
        try:
            stage_handle.put(
                local_file_name=environment_file_path,
                stage_location=f"/{repo_name}",
                overwrite=True,
                auto_compress=False,
            )
        except Exception:
            logger.error(f"Error while uploading file {ENVIRONMENT_FILE_PATH} to stage...")
            return False

    for i in range(0, num_steps):
        notebook_file = find_notebook_file(i, notebook_file_directory)
        if notebook_file is None:
            CONSOLE_MANGAER.safe_print(
                "Error while finding notebook files. Download directory seems to be corrupt", color="red"
            )
            CONSOLE_MANGAER.safe_print(
                f"Please reload the demo using load_demo('{demo_name}', refresh_demo=True).", color="red"
            )
            return False

        notebook_file_path = os.path.join(
            demo_directory,
            NOTEBOOK_DIR,
            notebook_file,
        )
        try:
            stage_handle.put(
                local_file_name=notebook_file_path,
                stage_location=f"/{repo_name}",
                overwrite=True,
                auto_compress=False,
            )
        except Exception as e:
            logger.error(f"Error while uploading file {notebook_file} to stage...")
            raise e
        notebook_name = get_notebook_name_from_file_name(notebook_file, demo_name)

        notebook = Notebook(
            name=f"{notebook_name}",
            comment=f"Notebook created for Snowflake demo {demo_name}",
            query_warehouse=DEMO_WAREHOUSE_NAME,
            fromLocation=f"@{DEMO_STAGE_NAME}/{repo_name}",
            main_file=notebook_file,
        )
        try:
            CONSOLE_MANGAER.safe_print(
                f"[yellow]Creating notebook[/yellow] [green]{notebook_name}[/green]...", color="yellow", end=""
            )
            notebook_handle = (
                root.databases[DEMO_DATABASE_NAME]
                .schemas[DEMO_SCHEMA_NAME]
                .notebooks.create(notebook, mode=CreateMode.or_replace)
            )
            notebook_handle.add_live_version(from_last=True)
            CONSOLE_MANGAER.safe_print("✅", color="green", bold=True)
        except Exception as e:
            CONSOLE_MANGAER.safe_print("❌", color="red", bold=True)
            logger.error(f"Error while creating notebook {notebook_name}...")
            raise e
    return True


def cleanup_demo(
    demo_name: str,
    num_steps: int,
    root: Root,
) -> None:
    """Cleanup the demo by deleting the demo notebook created and deleting the downloaded files.

    Parameters
    __________
      demo_name: The name of the demo.
      num_steps: The number of steps in the demo.
      root: The root connection to Snowflake.
    """
    logger.info(f"Cleaning up demo {demo_name}")
    CONSOLE_MANGAER.safe_print(f"[yellow]Deleting demo[/yellow] [green]{demo_name}[/green]...", color="yellow")
    demo_directory = get_demo_directory(demo_name)
    notebook_file_directory = os.path.join(demo_directory, NOTEBOOK_DIR)
    for i in range(0, num_steps):
        notebook_file = find_notebook_file(i, notebook_file_directory)
        if notebook_file is None:
            continue

        notebook_name = get_notebook_name_from_file_name(notebook_file, demo_name)

        try:
            CONSOLE_MANGAER.safe_print(
                f"[yellow]Deleting notebook[/yellow] [green]{notebook_name}[/green]...", color="yellow", end=""
            )
            root.databases[DEMO_DATABASE_NAME].schemas[DEMO_SCHEMA_NAME].notebooks[notebook_name].drop(
                if_exists=True,
            )
            CONSOLE_MANGAER.safe_print("✅", color="green", bold=True)
        except Exception as e:
            CONSOLE_MANGAER.safe_print("❌", color="red", bold=True)
            logger.error(f"Error while deleting notebook {notebook_name}...")
            raise e

    if os.path.exists(demo_directory):
        CONSOLE_MANGAER.safe_print(
            f"[yellow]Deleting downloaded files for demo[/yellow] [green]{demo_name}[/green]...", color="yellow", end=""
        )
        shutil.rmtree(demo_directory)
        CONSOLE_MANGAER.safe_print("✅", color="green", bold=True)


def get_notebook_file_directory(demo_name: str) -> str:
    """Get the directory containing the notebooks for the demo.

    Parameters
    __________
      demo_name: The name of the demo.

    Returns
    _______
      The directory containing the notebooks for the demo.
    """
    demo_mapping = read_demo_mapping_with_cache()
    demo_info = demo_mapping[demo_name]
    data_directory_file_path = os.path.join(os.path.dirname(__file__), DATA_DIR)
    repo_name = get_repo_name_from_url(demo_info[DEMO_REPO_URL_COLUMN])
    if repo_name is None:
        raise ValueError("Invalid repo URL")
    demo_directory = os.path.join(data_directory_file_path, repo_name)
    return os.path.join(demo_directory, NOTEBOOK_DIR)


def get_demo_directory(demo_name: str) -> str:
    """Get the directory containing the demo.

    Parameters
    __________
      demo_name: The name of the demo.

    Returns
    _______
      The directory containing the demo.
    """
    demo_mapping = read_demo_mapping_with_cache()
    demo_info = demo_mapping[demo_name]
    data_directory_file_path = os.path.join(os.path.dirname(__file__), DATA_DIR)
    repo_name = get_repo_name_from_url(demo_info[DEMO_REPO_URL_COLUMN])
    if repo_name is None:
        raise ValueError("Invalid repo URL")
    return os.path.join(data_directory_file_path, repo_name)


def create_notebook_url_from_demo_name(
    demo_name: str, demo_connection: DemoConnection, step: int = 0
) -> Tuple[bool, str]:
    """Create a URL for the notebook in the demo.

    Parameters
    __________
      demo_name: The name of the demo.
      step: The step number of the notebook.

    Returns
    _______
      The URL of the notebook.
    """
    notebook_file_directory = get_notebook_file_directory(demo_name)
    notebook_file = find_notebook_file(step, notebook_file_directory)
    if notebook_file is None:
        CONSOLE_MANGAER.safe_print(
            "Error while finding notebook files. Download directory seems to be corrupt", color="red"
        )
        CONSOLE_MANGAER.safe_print(
            f"Please reload the demo using load_demo('{demo_name}', refresh_demo=True).", color="red"
        )
        return (False, "")
    notebook_name = get_notebook_name_from_file_name(notebook_file, demo_name)
    return (
        True,
        f"https://app.snowflake.com/{demo_connection.get_organization().lower()}/{demo_connection.get_account().lower()}/#/notebooks/{DEMO_DATABASE_NAME}.{DEMO_SCHEMA_NAME}.{notebook_name.upper()}",
    )


def cleanup_demos_download() -> None:
    """Cleanup the downloaded demo files."""
    logger.info("Cleaning up demo downloads directory")
    data_directory_file_path = os.path.join(os.path.dirname(__file__), DATA_DIR)
    if os.path.exists(data_directory_file_path):
        CONSOLE_MANGAER.safe_print("Deleting downloaded demo files...", color="yellow", end="")
        shutil.rmtree(data_directory_file_path)
        CONSOLE_MANGAER.safe_print("✅", color="green", bold=True)
