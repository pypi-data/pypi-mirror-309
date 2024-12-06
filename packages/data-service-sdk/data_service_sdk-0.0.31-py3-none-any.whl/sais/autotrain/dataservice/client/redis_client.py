import redis
from loguru import logger
import time

from sais.autotrain.dataservice.cfg.env import CustomEnv


class RedisClient:
    def __init__(self, host=None, port=None, db=None, password=None):
        self.host = host or CustomEnv.get_redis_host()
        self.password = password or CustomEnv.get_redis_password()
        self.port = port or CustomEnv.get_redis_port()
        self.db = db or CustomEnv.get_redis_db()
        self.pool = None
        self.r = None
        self.connect()

    def connect(self):
        try:
            logger.info("Connecting to Redis...")
            self.pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password)
            self.r = redis.Redis(connection_pool=self.pool)
            r_res = self.r.ping()
            if not r_res:
                logger.error("Failed to connect to Redis, exiting with code 1")
                exit(1)
            logger.info("Connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis, error={e}")
            self.reconnect()

    def reconnect(self):
        logger.info("Attempting to reconnect to Redis...")
        time.sleep(5)  # Wait before reconnecting
        self.connect()

    def hgetall(self, key):
        try:
            return self.r.hgetall(key)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            logger.error(f"Redis connection error: {e}")
            self.reconnect()
            return self.hgetall(key)

    def hset(self, key, field, value):
        try:
            return self.r.hset(key, field, value)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            logger.error(f"Redis connection error: {e}")
            self.reconnect()
            return self.hset(key, field, value)

    def zrangebyscore(self, key, min_score, max_score):
        try:
            return self.r.zrangebyscore(key, min_score, max_score)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            logger.error(f"Redis connection error: {e}")
            self.reconnect()
            return self.zrangebyscore(key, min_score, max_score)

    def zadd(self, key, score, value):
        try:
            return self.r.zadd(key, {value: score})
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            logger.error(f"Redis connection error: {e}")
            self.reconnect()
            return self.zadd(key, score, value)

    def zdel(self, key, score, value):
        try:
            return self.r.zrem(key, {value: score})
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            logger.error(f"Redis connection error: {e}")
            self.reconnect()
            return self.zadd(key, score, value)


    def zremrangebyscore(self, key, min, max):
        try:
            return self.r.zremrangebyscore(key, min, max)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            logger.error(f"Redis connection error: {e}")
            self.reconnect()
            return self.zremrangebyscore(key, min, max)

    def zupdatebyscore(self, key, score, value):
        try:
            self.zremrangebyscore(key, score, score)
            self.zadd(key, score, value)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            logger.error(f"Redis connection error: {e}")
            self.reconnect()
            return self.zupdatebyscore(key, score, value)


    def zcard(self, key):
        try:
            return self.r.zcard(key)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            logger.error(f"Redis connection error: {e}")
            self.reconnect()
            return self.zcard(key)

    def set(self, key, value, expire_sec):
        try:
            return self.r.set(key, value, expire_sec)  # Set the key with an expiration time of 7 days
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            logger.error(f"Redis connection error: {e}")
            self.reconnect()
            return self.set(key, value, expire_sec)

    def delete(self, key):
        try:
            return self.r.delete(key)  # Set the key with an expiration time of 7 days
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            logger.error(f"Redis connection error: {e}")
            self.reconnect()
            return self.delete(key)


# Instantiate the Redis client
# redis_client = RedisClient()