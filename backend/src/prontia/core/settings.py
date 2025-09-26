from starlette.config import Config


ENV_FILE = ".env"


class OpenAiSettings:
    conf = Config(env_file=ENV_FILE, env_prefix="OPENAI_")
    ENDPOINT: str = conf(key="ENDPOINT", cast=str)
    DEPLOYMENT: str = conf("DEPLOYMENT", cast=str)
    APIKEY: str = conf("APIKEY", cast=str)


class CosmosdbSettings:
    conf = Config(env_file=ENV_FILE, env_prefix="COSMOSDB_")
    ENDPOINT: str = conf("ENDPOINT", cast=str)
    ACCOUNTKEY: str = conf("ACCOUNTKEY", cast=str)
    DATABASE: str = conf("DATABASE", cast=str)


class Settings:
    conf = Config(env_file=ENV_FILE)
    LOGLEVEL: str = conf("LOGLEVEL", cast=str, default="INFO")
    openai = OpenAiSettings()
    cosmosdb = CosmosdbSettings()


settings = Settings()
