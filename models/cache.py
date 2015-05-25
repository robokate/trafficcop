__author__ = 'kate'

import redis

import models.urlencoder

class Cache(object):
    r_server = redis.Redis("localhost")
    encoder = models.urlencoder.UrlEncoder()

    @staticmethod
    def get(key):
        return Cache.r_server.get(key)

    @staticmethod
    def put_url(url):
        if not url.startswith('http://'):
            url = "http://{0}".format(url)
        short_url = Cache.encoder.encode_url(Cache.get_next_key())
        Cache.r_server.set(short_url, url, nx=True)
        return short_url

    @staticmethod
    def dump():
        return Cache.r_server.keys()

    @staticmethod
    def is_valid_api_key(api_key):
        return Cache.r_server.sismember("api_keys", api_key)

    @staticmethod
    def get_next_key():
        return Cache.r_server.dbsize()

