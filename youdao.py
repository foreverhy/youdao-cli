#! /usr/bin/env python3
# coding:utf-8

# http://fanyi.youdao.com/openapi?path=data-mode

import sys
import requests
import json

API_KEY = ""
KEYFROM = ""
DOCTYPE = "json"
VERSION = "1.1"


ERROR_MSG = {
    0: "Normal", 20: "Invalid query length", 30: "Query error", 40: "Unsupported language", 50: "Invalid API key",
    60: "No result",
}


URL = "http://fanyi.youdao.com/openapi.do?keyfrom=" + KEYFROM + "&key=" + API_KEY +  "&type=data&doctype=" \
    + DOCTYPE + "&version=" + VERSION + "&q="

def error(msg):
    print("ERROR: " + msg)

class YoudaoError(Exception):
    def __init__(self, msgno):
        self.msg = ERROR_MSG[msgno]

    def __str__(self):
        return repr(self.msg)

class Youdao(object):
    def __init__(self, query):
        self.url = URL + query
        self.response = None

    def search(self):
        try:
            return  requests.get(self.url).text
        except:
            raise YoudaoError("Fail to connect server")

    def parse(self, resp):
        result = json.loads(resp)
        errno = result['errorCode']
        if 0 == errno:
            print('--------')
            for item in result['translation']:
                print(item)
            if 'basic' in result.keys():
                no = 1
                for item in result['basic']['explains']:
                    item = item.split('；')
                    for expl in item:
                        print(str(no) + ": " + expl)
                        no += 1
            print('--------')
        else:
            raise YoudaoError(errno)

    def translate(self):
        self.parse(self.search())


def main():
    if len(sys.argv) != 2:
        return error("USAGE: " + __file__ + " query")
    youdao = Youdao(sys.argv[1])
    youdao.translate()


if __name__ == '__main__':
    main()
