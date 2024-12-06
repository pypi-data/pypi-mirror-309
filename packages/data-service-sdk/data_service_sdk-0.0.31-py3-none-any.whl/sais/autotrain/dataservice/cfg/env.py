import os


class CustomEnv:
    def __init__(self):
        pass

    @classmethod
    def get_redis_host(cls) -> str:
        return "localhost" if os.getenv("REDIS_HOST") is None else os.getenv("REDIS_HOST")

    @classmethod
    def get_redis_password(cls) -> str:
        return "default_password" if os.getenv("REDIS_PASSWORD") is None else os.getenv("REDIS_PASSWORD")

    @classmethod
    def get_redis_port(cls) -> int:
        return 6379 if os.getenv("REDIS_PORT") is None else os.getenv("REDIS_PORT")

    @classmethod
    def get_redis_db(cls) -> int:
        return 0 if os.getenv("REDIS_DB") is None else os.getenv("REDIS_DB")

    @classmethod
    def get_server_port(cls) -> str:
        return os.getenv("SERVER_PORT") if os.getenv("SERVER_PORT") else "10019"