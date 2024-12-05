import logging

from typing import Any, Dict, Optional, Type, cast

from snowflake.connector.cursor import SnowflakeCursor
from snowflake.core import CreateMode, Root
from snowflake.core.database import Database
from snowflake.core.schema import Schema
from snowflake.core.stage import Stage
from snowflake.core.warehouse import Warehouse
from snowflake.demos._constants import (
    DEMO_DATABASE_NAME,
    DEMO_SCHEMA_NAME,
    DEMO_STAGE_NAME,
    DEMO_WAREHOUSE_NAME,
)
from snowflake.demos._environment_detection import CONSOLE_MANGAER
from snowflake.demos._telemetry import ApiTelemetryClient
from snowflake.snowpark.session import Session


logger = logging.getLogger(__name__)


class SingletonMeta(type):
    _instances: Dict[Type[Any], Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> "DemoConnection":
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DemoConnection(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._root: Optional[Root] = None
        self._telemetry_client: Optional[ApiTelemetryClient] = None
        self._organization = None
        self._account = None

    def setup(self) -> None:
        if not self._root:
            self._root = self._create_root()
            cursor = self._get_cursor()
            logger.info("Creating new database, schema and warehouse for demo setup")
            try:
                CONSOLE_MANGAER.safe_print(
                    "[yellow]Using[/yellow] [red]ACCOUNTADMIN[/red] [yellow]role...[/yellow]", color="yellow", end=""
                )
                cursor.execute("USE ROLE ACCOUNTADMIN")
                CONSOLE_MANGAER.safe_print("✅", color="green", bold=True)
            except Exception as e:
                CONSOLE_MANGAER.safe_print("❌", color="red", bold=True)
                logger.error(
                    "Error while using ACCOUNTADMIN role. Make sure the user have permissions to use ACCOUNTADMIN role."
                )
                raise e

            try:
                CONSOLE_MANGAER.safe_print(
                    f"[yellow]Creating Database[/yellow] [green]{DEMO_DATABASE_NAME}[/green]...", color="yellow", end=""
                )
                self._root.databases.create(
                    Database(name=DEMO_DATABASE_NAME, comment="Database created for Snowflake demo setup"),
                    mode=CreateMode.or_replace,
                )
                CONSOLE_MANGAER.safe_print("✅", color="green", bold=True)
            except Exception as e:
                CONSOLE_MANGAER.safe_print("❌", color="red", bold=True)
                logger.error(f"Error while creating database {DEMO_DATABASE_NAME}...")
                raise e

            try:
                CONSOLE_MANGAER.safe_print(
                    f"[yellow]Creating Schema[/yellow] [green]{DEMO_SCHEMA_NAME}[/green]...", color="yellow", end=""
                )
                self._root.databases[DEMO_DATABASE_NAME].schemas.create(
                    Schema(name=DEMO_SCHEMA_NAME, comment="Schema created for Snowflake demo setup"),
                    mode=CreateMode.or_replace,
                )
                CONSOLE_MANGAER.safe_print("✅", color="green", bold=True)
            except Exception as e:
                CONSOLE_MANGAER.safe_print("❌", color="red", bold=True)
                logger.error(f"Error while creating schema {DEMO_SCHEMA_NAME}...")
                raise e

            try:
                CONSOLE_MANGAER.safe_print(
                    f"[yellow]Creating Warehouse[/yellow] [green]{DEMO_WAREHOUSE_NAME}[/green]...",
                    color="yellow",
                    end="",
                )
                warehouse = Warehouse(
                    name=DEMO_WAREHOUSE_NAME,
                    comment="Warehouse created for Snowflake demo setup",
                    warehouse_size="SMALL",
                    auto_suspend=500,
                )
                self._root.warehouses.create(warehouse, mode=CreateMode.or_replace)
                CONSOLE_MANGAER.safe_print("✅", color="green", bold=True)
            except Exception as e:
                CONSOLE_MANGAER.safe_print("❌", color="red", bold=True)
                logger.error(f"Error while creating warehouse {DEMO_WAREHOUSE_NAME}...")
                raise e

            try:
                CONSOLE_MANGAER.safe_print(
                    f"[yellow]Creating Stage[/yellow] [green]{DEMO_STAGE_NAME}[/green]...", color="yellow", end=""
                )
                stage = Stage(name=DEMO_STAGE_NAME, comment="Stage created for Snowflake demo setup")
                self._root.databases[DEMO_DATABASE_NAME].schemas[DEMO_SCHEMA_NAME].stages.create(
                    stage,
                    mode=CreateMode.or_replace,
                )
                CONSOLE_MANGAER.safe_print("✅", color="green", bold=True)
            except Exception as e:
                CONSOLE_MANGAER.safe_print("❌", color="red", bold=True)
                logger.error(f"Error while creating stage {DEMO_STAGE_NAME}...")
                raise e

            try:
                organization: Optional[SnowflakeCursor] = self._get_cursor().execute(
                    "SELECT CURRENT_ORGANIZATION_NAME()"
                )
                if organization:
                    self._organization = organization.fetchone()[0]  # type: ignore[index]
                else:
                    CONSOLE_MANGAER.safe_print(
                        "Organization name not found. Make sure the user have sufficient permission.", color="red"
                    )
                    raise ValueError("Organization name not found.")
            except Exception as e:
                logger.error("Error while fetching organization name...")
                raise e

            try:
                account: Optional[SnowflakeCursor] = self._get_cursor().execute("SELECT CURRENT_ACCOUNT_NAME()")
                if account:
                    self._account = account.fetchone()[0]  # type: ignore[index]
                else:
                    CONSOLE_MANGAER.safe_print(
                        "Account name not found. Make sure the user have sufficient permission.", color="red"
                    )
                    raise ValueError("Account name not found.")
            except Exception as e:
                logger.error("Error while fetching account name...")
                raise e

    def get_root(self) -> Root:
        if self._root is None:
            raise ValueError("Root not set. Please call setup() first.")
        return self._root

    def teardown(self) -> None:
        # scenario where teardown is called without load_demo being called first
        if self._root is None:
            self._root = self._create_root()
        logger.info("Deleting database, schema and warehouse created for demo setup")
        cursor = self._get_cursor()
        try:
            CONSOLE_MANGAER.safe_print(
                "[yellow]Using[/yellow] [red]ACCOUNTADMIN[/red] [yellow]role...[/yellow]", color="yellow", end=""
            )
            cursor.execute("USE ROLE ACCOUNTADMIN")
            CONSOLE_MANGAER.safe_print("✅", color="green", bold=True)
        except Exception as e:
            CONSOLE_MANGAER.safe_print("❌", color="red", bold=True)
            logger.error("Error while using ACCOUNTADMIN role...")
            raise e

        try:
            CONSOLE_MANGAER.safe_print(
                f"[yellow]Dropping Database[/yellow] [green]{DEMO_DATABASE_NAME}[/green]...", color="yellow", end=""
            )
            self._root.databases[DEMO_DATABASE_NAME].drop(if_exists=True)
            CONSOLE_MANGAER.safe_print("✅", color="green", bold=True)
        except Exception as e:
            CONSOLE_MANGAER.safe_print("❌", color="red", bold=True)
            logger.error(f"Error while dropping database {DEMO_DATABASE_NAME}...")
            raise e

        try:
            CONSOLE_MANGAER.safe_print(
                f"[yellow]Dropping Warehouse[/yellow] [green]{DEMO_WAREHOUSE_NAME}[/green]...",
                color="yellow",
                end="",
            )
            self._root.warehouses[DEMO_WAREHOUSE_NAME].drop(if_exists=True)
            CONSOLE_MANGAER.safe_print("✅", color="green", bold=True)
        except Exception as e:
            CONSOLE_MANGAER.safe_print("❌", color="red", bold=True)
            logger.error(f"Error while dropping warehouse {DEMO_WAREHOUSE_NAME}...")
            raise e
        self._root = None

    def _create_root(self) -> Root:
        logger.info("Creating a new root connection")
        try:
            CONSOLE_MANGAER.safe_print(
                "[yellow]Connecting to[/yellow] [magenta]Snowflake[/magenta]...", color="yellow", end=""
            )
            root = Root(Session.builder.create())
            CONSOLE_MANGAER.safe_print("✅", color="green", bold=True)
        except Exception as e:
            CONSOLE_MANGAER.safe_print("❌", color="red", bold=True)
            logger.error("Error while connecting to snowflake...")
            raise e
        self._telemetry_client = ApiTelemetryClient(root.connection)
        return root

    def get_account(self) -> str:
        if self._account is None:
            raise ValueError("Account not set. Please call setup() first.")
        else:
            return cast(str, self._account)  # type: ignore[unreachable]

    def get_organization(self) -> str:
        if self._organization is None:
            raise ValueError("Organization not set. Please call setup() first.")
        else:
            return cast(str, self._organization)  # type: ignore[unreachable]

    def get_telemetry_client(self) -> Optional[ApiTelemetryClient]:
        return self._telemetry_client

    def _get_cursor(self) -> SnowflakeCursor:
        if self._root is None:
            raise ValueError("Root is not set. Please call setup() first.")
        return self._root.connection.cursor()
