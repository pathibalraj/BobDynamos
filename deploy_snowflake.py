"""
deploy_snowflake.py
Executes test.sql against Snowflake using credentials from environment variables.

Required environment variables:
  SNOWFLAKE_ACCOUNT    e.g. vtpifwq-gi48711
  SNOWFLAKE_USER       e.g. PATTIBALRAJ
  SNOWFLAKE_PASSWORD   your Snowflake password
  SNOWFLAKE_WAREHOUSE  e.g. COMPUTE_WH
  SNOWFLAKE_DATABASE   e.g. BOB_TEST
  SNOWFLAKE_SCHEMA     e.g. BOB_SF
"""

import os
import logging
import snowflake.connector

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

SQL_FILE = "test.sql"

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

    with open(SQL_FILE, "r", encoding="utf-8") as f:
        sql = f.read().strip()

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
        logger.info("Executing: %s", SQL_FILE)
        cursor.execute(sql)
        logger.info("Deployment successful.")
    except Exception:
        logger.error("Deployment failed.", exc_info=True)
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    main()
