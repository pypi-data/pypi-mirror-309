from urllib.parse import quote_plus

import sqlalchemy as sa
import configparser
from pathlib import Path
from . import models 


def __create_sqlalchemy_url(
        dialect: str,
        username: str = None,
        password: str = None,
        host: str = None,
        port: int = None,
        database: str = None,
        driver: str = None,
        **options
) -> str:
    """
    Create a SQLAlchemy connection URL.

    :param dialect: Database dialect, e.g., 'postgresql', 'mysql', 'mssql', etc.
    :param username: Username for the database (optional).
    :param password: Password for the database (optional).
    :param host: Database host address.
    :param port: Port number for the database (optional).
    :param database: Database name (optional).
    :param driver: Optional driver, e.g., 'psycopg2' for PostgreSQL.
    :param options: Additional URL parameters, such as {'sslmode': 'require'}.
    :return: A SQLAlchemy connection URL.
    """
    # Initialize the base URL with the dialect and optional driver
    url = f"{dialect}"
    if driver:
        url += f"+{driver}"
    url += "://"

    # Add the username and password if provided
    if username:
        url += f"{username}"
        if password:
            url += f":{quote_plus(password)}"
        url += "@"

    # Add the host and port if provided
    url += host
    if port:
        url += f":{port}"

    # Add the database name if provided
    if database:
        url += f"/{database}"
    else:
        url += "/"

    # Append any additional options as query parameters
    if options:
        url += "?" + "&".join(f"{key}={quote_plus(str(value))}" for key, value in options.items())

    return url


def get_config(name: str) -> dict[str, str]:
    config = configparser.ConfigParser()
    config.read(f'{Path.home()}/.jupysql/connections.ini')

    return dict(config.items(name))

def get_url(name: str) -> str:
    config = configparser.ConfigParser()
    config.read(f'{Path.home()}/.jupysql/connections.ini')
    config = config[name]

    return __create_sqlalchemy_url(
        dialect=config.get('drivername'),
        host=config.get('host'),
        port=config.get('port'),
        database=config.get('database'),
        username=config.get('username'),
        password=config.get('password'),
    )

def get_mssql(name: str) -> models.MSSQLConfig:
    config = get_config(name)
    return models.MSSQLConfig(**config)


def get_engine(name: str) -> sa.Engine:
    url = get_url(name)
    return sa.create_engine(url)
