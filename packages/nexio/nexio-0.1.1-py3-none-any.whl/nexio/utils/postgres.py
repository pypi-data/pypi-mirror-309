import os
import psycopg2
from dotenv import load_dotenv, find_dotenv
from pydantic import BaseModel, Field

from nexio.exceptions import MissingEnvironmentVariableError


class PostgresCredentials(BaseModel):
    db_user: str = Field(description="PostgreSQL user name", default="")
    db_password: str = Field(description="PostgreSQL user password", default="")
    db_host: str = Field(description="PostgreSQL host", default="")
    db_port: str = Field(description="PostgreSQL port", default="")
    db_name: str = Field(description="PostgreSQL name", default="")

    def _validate_env_vars(self):
        for var_key, var_value in self.model_dump().items():
            if var_key not in os.environ:
                raise MissingEnvironmentVariableError(f"Missing environment variable {var_key}")

    def get_url(self):
        self._validate_env_vars()
        return f"postgres://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class Postgres:
    def __init__(self):
        load_dotenv(find_dotenv())
        self._credentials = PostgresCredentials(
            db_user=os.getenv("db_user", ""),
            db_password=os.getenv("db_password", ""),
            db_host=os.getenv("db_host", ""),
            db_name=os.getenv("db_name", ""),
            db_port=os.getenv("db_port", ""),
        )
        self.url = self._credentials.get_url()
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(self.url)

        except psycopg2.Error as e:
            raise e


def main():
    postgres = Postgres()
    postgres.connect()
    print(postgres.conn)


if __name__ == '__main__':
    main()
