from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class DatabaseConfig(BaseSettings):
    """
    Configuration class for database connection parameters. Parameters are by default
    loaded from the environment variables.

    Attributes:
        db_user (str): The username for connecting to the database.
        db_password (str): The password for connecting to the database.
        db_name (str): The name of the database.
        db_host (str): The hostname or IP address of the database server.
        db_port (int): The port number for the database server. Default is 5432.
    """

    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int = Field(default=5432)

    model_config = SettingsConfigDict(
        str_min_length=1,
        extra="forbid",
        env_prefix="openfb_",
    )

    def to_uri(self) -> str:
        """
        Generates a PostgreSQL URI based on the configuration.

        Returns:
            str: The PostgreSQL URI string.
        """
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
