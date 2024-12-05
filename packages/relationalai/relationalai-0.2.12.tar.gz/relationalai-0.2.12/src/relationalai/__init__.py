import textwrap
from typing import cast
from .clients import config as cfg
from . import clients
from . import dsl
from . import debugging
from . import metamodel
from . import rel
from .loaders import csv
from . import analysis
from . import tools
import importlib.metadata
from snowflake.connector import SnowflakeConnection

import sys
import rich

version = sys.version_info[:2]
three12warning = "You probably got it because you are using Python 3.12.\n    " if version == (3, 12) else ""
rich.print(textwrap.dedent(f"""
    [red]This version of the RelationalAI Python library is out of date and is no longer recommended.
    {three12warning}As of v0.3.0, only Python 3.9, 3.10, and 3.11 are supported.[/red]
    
    [yellow]Please install a supported version of Python and try again.[/yellow]
    """
))


# Set up global exception handler for debugging
debugging.setup_exception_handler()

__version__ = importlib.metadata.version(__package__ or __name__)

def Model(
    name: str,
    *,
    profile: str | None = None,
    config: cfg.Config | None = None,
    dry_run: bool = False,
    debug=None,
    connection: SnowflakeConnection | None = None,
):
    config = config or cfg.Config(profile=profile)
    if debug is None:
        debug = config.get("debug", False)
    if debug:
        from relationalai.tools.debugger_client import start_debugger_session
        start_debugger_session() # @TODO: add config / env vars / kwargs for debug_host and debug_port
    if not config.file_path:
        if cfg.legacy_config_exists():
            message = (
                "Use `rai init` to migrate your configuration file "
                "to the new format (raiconfig.toml)"
            )
        else:
            message = "No configuration file found. Please run `rai init` to create one."
        raise Exception(message)
    if config.get("platform") is None:
        config.set("platform", "snowflake")
    platform = config.get("platform")
    if platform != "snowflake" and connection is not None:
        raise ValueError("The `connection` parameter is only supported with the Snowflake platform")
    dry_run = cast(bool, dry_run or config.get("compiler.dry_run", False))
    if platform == "azure":
        return clients.azure.Graph(
            name, profile=profile, config=config, dry_run=dry_run
        )
    elif platform == "snowflake":
        return clients.snowflake.Graph(
            name, profile=profile, config=config, dry_run=dry_run, connection=connection
        )
    else:
        raise Exception(f"Unknown platform: {platform}")

def Resources(profile:str|None=None, config:cfg.Config|None=None):
    config = config or cfg.Config(profile)
    platform = config.get("platform", "snowflake")
    if platform == "azure":
        return clients.azure.Resources(config=config)
    elif platform == "snowflake":
        return clients.snowflake.Resources(config=config)
    else:
        raise Exception(f"Unknown platform: {platform}")

def Graph(name:str, dry_run:bool=False):
    return Model(name, profile=None, dry_run=dry_run)

__all__ = ['Model', 'Resources', 'dsl', 'rel', 'debugging', 'metamodel', 'csv', 'analysis', 'tools']
