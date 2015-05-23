__author__ = 'kate'

import redis

class Cache(object):
    r_server = redis.Redis("localhost")

    @staticmethod
    def get(key):
        return Cache.r_server.get(key)

    @staticmethod
    def put(key, value):
        Cache.r_server.set(key, value, nx=True);
        return Cache.get(key)

    @staticmethod
    def dump():
        return Cache.r_server.keys()

    @staticmethod
    def is_valid_api_key(apikey):
        try:
            Cache.r_server.sismember("api_keys", apikey)
        except BaseException as e:
            print "{0} while {1}".format(e, "checking api key")
        return Cache.r_server.sismember("api_keys", apikey)

    @staticmethod
    def get_next_key():
        return Cache.r_server.dbsize() + 1

