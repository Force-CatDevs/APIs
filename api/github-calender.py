# -*- coding: UTF-8 -*-
import http.server

import requests
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


def getdata(name):
    gitpage = requests.get("https://github.com/" + name, verify=False)
    data = gitpage.text
    datadatereg = re.compile(r'data-date="(.*?)" data-level')
    datacountreg = re.compile(r'">(.*?) contribution.')
    datadate = datadatereg.findall(data)
    datacount = datacountreg.findall(data)
    datacount = [0 if i == 'No' else i for i in datacount]
    datacount = list(map(int, datacount))
    contributions = sum(datacount)
    datalist = []
    print(datadate)
    for index, item in enumerate(datadate):
        itemlist = {"date": item, "count": datacount[index]}
        datalist.append(itemlist)
    datalistsplit = list_split(datalist, 7)
    returndata = {
        "total": contributions,
        "contributions": datalistsplit
    }
    print(returndata)
    return returndata


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        if "?" in path:
            user = path.split('?')[1]
            data = getdata(user)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            data = {"code": "400", "msg": "Invalid Parameter", "param": {"user": "str"}}
            self.send_response(400)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        return


if __name__ == '__main__':
    host = ('localhost', 8888)
    server = HTTPServer(host, handler)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
