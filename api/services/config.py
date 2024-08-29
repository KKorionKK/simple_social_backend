from dotenv import find_dotenv, dotenv_values

env = dotenv_values(find_dotenv())

DB_NAME = env.get("DB_NAME")
PG_USER = env.get("PG_USER")
PG_PASSWORD = env.get("PG_PASSWORD")
DB_ADAPTER = env.get("DB_ADAPTER")
DB_HOST = env.get("DB_HOST")
DB_PORT = env.get("DB_PORT")


# Security
SECRET = "74cbaab21625e535d0ac221ed39ebeb48ca61a5aaaf07e7021c94249ef5a97ed"
ALGORITHM = "HS256"
SECURITY_TOKEN_EXPIRES = 30

# Caching
SUBS_COUNT_TO_CACHE = 500

# Redis
REDIS_HOST = env.get("REDIS_HOST")
REDIS_PORT = env.get("REDIS_PORT")
REDIS_PASSWORD = env.get("REDIS_PASSWORD")


def get_connection_string() -> str:
    return f"{DB_ADAPTER}://{PG_USER}:{PG_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
