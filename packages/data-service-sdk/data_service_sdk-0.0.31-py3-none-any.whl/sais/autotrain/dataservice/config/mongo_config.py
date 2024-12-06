import os
from pymongo import MongoClient
class MongoConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MongoConfig, cls).__new__(cls)
            cls._instance._initialize_from_env()
        return cls._instance

    def _initialize_from_env(self):
        self.host = os.getenv('MONGO_HOST', 'localhost')
        self.port = int(os.getenv('MONGO_PORT', 8087))
        self.user = os.getenv('MONGO_USER', "root")
        self.password = os.getenv('MONGO_PASSWORD', "yourPassword")
        self.__set_client()

    def set_config(self, host=None, port=None, user=None, password=None):
        if host:
            self.host = host
        if port:
            self.port = int(port)
        if user:
            self.user = user
        if password:
            self.password = password
        self.__set_client()
    def __set_client(self):
        mongo_url = f'mongodb://{self.user}:{self.password}@{self.host}:{self.port}'
        client = MongoClient(mongo_url,
                             serverSelectionTimeoutMS=30000,
                             connectTimeoutMS=30000)
        self.client = client

    def get_client(self):
        return self.client

    def close(self):
        if self.client:
            self.client.close()
            self.client = None


mongo_config = MongoConfig()