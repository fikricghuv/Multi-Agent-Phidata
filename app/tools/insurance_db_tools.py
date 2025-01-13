from phi.tools.postgres import PostgresTools
from app.config.settings import load_environment_variables

env_vars = load_environment_variables()
password = env_vars["PASSWORD"]
user = env_vars["USER"]
db_name = env_vars["DB_NAME"]
host = env_vars["HOST"]

postgres_insuranceDB_tools = PostgresTools(
    host=host,
    port=5432,
    db_name=db_name,
    user=user,
    password=password
)