# coding:utf8
import hashlib

__author__ = 'pangguangde'


class StringUtil(object):

    @staticmethod
    def generate_id(ip, port):
        return hashlib.md5('%s:%s' % (ip, port)).hexdigest()

    @staticmethod
    def md5_encode(string):
        if type(string) == unicode:
            string = string.encode('utf8')
        return hashlib.md5(string).hexdigest()
