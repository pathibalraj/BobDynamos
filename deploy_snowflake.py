"""
deploy_snowflake.py
Discovers and executes all *.sql files in the repository against Snowflake.
Files are executed in alphabetical order.

Required environment variables:
  SNOWFLAKE_ACCOUNT    e.g. account-identifier
  SNOWFLAKE_USER       e.g. MY_USER
  SNOWFLAKE_PASSWORD   your Snowflake password
  SNOWFLAKE_WAREHOUSE  e.g. COMPUTE_WH
  SNOWFLAKE_DATABASE   e.g. MY_DATABASE
  SNOWFLAKE_SCHEMA     e.g. MY_SCHEMA
"""

import os
import glob
import logging
import snowflake.connector

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise EnvironmentError(f"Required environment variable '{name}' is not set.")
    return value


def main() -> None:
    account   = get_required_env("SNOWFLAKE_ACCOUNT")
    user      = get_required_env("SNOWFLAKE_USER")
    password  = get_required_env("SNOWFLAKE_PASSWORD")
    warehouse = get_required_env("SNOWFLAKE_WAREHOUSE")
    database  = get_required_env("SNOWFLAKE_DATABASE")
    schema    = get_required_env("SNOWFLAKE_SCHEMA")

    # Discover all *.sql files recursively, sorted alphabetically
    sql_files = sorted(glob.glob("**/*.sql", recursive=True))

    if not sql_files:
        logger.info("No SQL files found. Nothing to deploy.")
        return

    logger.info("Found %d SQL file(s) to execute: %s", len(sql_files), sql_files)

    logger.info("Connecting to Snowflake account: %s", account)
    conn = snowflake.connector.connect(
        account=account,
        user=user,
        password=password,
        warehouse=warehouse,
        database=database,
        schema=schema,
    )

    try:
        cursor = conn.cursor()
        for sql_file in sql_files:
            with open(sql_file, "r", encoding="utf-8") as f:
                sql = f.read().strip()

            if not sql:
                logger.info("Skipping empty file: %s", sql_file)
                continue

            logger.info("Executing: %s", sql_file)
            try:
                cursor.execute(sql)
                logger.info("Success: %s", sql_file)
            except Exception:
                logger.error("Failed: %s", sql_file, exc_info=True)
                raise

    finally:
        conn.close()
        logger.info("Snowflake connection closed.")


if __name__ == "__main__":
    main()
