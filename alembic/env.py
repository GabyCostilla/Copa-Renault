# Copa-Renault/alembic/env.py
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
from app import db
target_metadata = db.Model.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# Ensure the current working directory is correct, as Alembic expects it to be
if not context.is_offline_mode():
    # Ensure SQLAlchemy engine is created from configuration
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    # Connect to the database using the SQLAlchemy engine
    connection = engine.connect()
    # Attach the connection to the Alembic context
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )
