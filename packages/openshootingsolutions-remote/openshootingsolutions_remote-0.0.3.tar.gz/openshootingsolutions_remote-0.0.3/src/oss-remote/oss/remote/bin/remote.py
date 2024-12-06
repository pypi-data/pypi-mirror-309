from typing import Optional

from oss.core.bin.argumentparser import ArgumentParser
from oss.core.log import Log
from oss.remote.app import RemoteApp
from oss.remote.remotes.type import RemoteType
from pydantic import BaseModel, Field, ValidationError, field_validator

# Activate module wide logging
logger = Log.get_logger_function()(__name__)


class LaunchArguments(BaseModel):
    model_config = {
        "extra": "ignore",  # Prevent unwanted extra fields from being added to this class
    }

    worker_config: Optional[str] = Field(
        examples=[],
        description="Filepath to the .env worker configuration file",
        default=None,
    )

    broker_host: Optional[str] = Field(
        examples=["localhost", "127.0.0.1", "broker.example"],
        description="Hostname, FQDN or IP address of the message broker",
        default="localhost",
    )

    broker_port: Optional[int] = Field(
        examples=[5671, 5672],
        description="Port number of the message broker",
        default=5672,
    )

    remote_type: str = Field(
        examples=["keypad", "buttonpad"],
        description="The type of remote this worker needs to handle",
    )

    @field_validator("worker_config")
    @classmethod
    def validate_worker_config(cls, worker_config: str) -> str:
        if worker_config == "":
            raise ValueError("Worker config cannot be empty")
        if not worker_config.endswith(".env"):
            raise ValueError("Worker config must be a .env file")
        return worker_config

    @field_validator("broker_host")
    @classmethod
    def validate_broker_host(cls, broker_host: str) -> str:
        if broker_host == "":
            raise ValueError("Broker host cannot be empty")
        return broker_host

    @field_validator("broker_port")
    @classmethod
    def validate_broker_port(cls, broker_port: int) -> int:
        if broker_port < 1 or broker_port > 65535:
            raise ValueError("Broker port must be between 1 and 65535")
        return broker_port

    @field_validator("remote_type")
    @classmethod
    def supported_remote_types(cls, remote_type: str) -> str:
        try:
            if not RemoteType[remote_type.upper()]:
                raise ValueError(f"Unsupported remote_type '{remote_type}'")
        except KeyError:
            raise ValueError(f"Unsupported remote_type '{remote_type}'")
        return remote_type


# The default entrypoint for this application
def cli() -> None:
    # Retrieve the launch arguments for this application
    try:
        launch_arguments: LaunchArguments = ArgumentParser.parse_arguments(launch_argument_model=LaunchArguments)
    except ValidationError as error:
        logger.critical(f"There was an error while validating the launch arguments. {error}")

    # Get the remote type from the launch arguments. Then start the app passing the remote type
    remote_type: RemoteType = RemoteType[str(launch_arguments.remote_type).upper()]
    remote_app: RemoteApp = RemoteApp(remote=remote_type)
    remote_app.run()


# The app was not started via the CLI-entrypoint
# Call the CLI function so we have a consistent way of starting the application
if __name__ == "__main__":
    cli()
