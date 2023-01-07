# -*- coding: UTF-8 -*-

import requests
from urllib import parse
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
    for index, item in enumerate(datadate):
        itemlist = {"date": item, "count": datacount[index]}
        datalist.append(itemlist)
    datalistsplit = list_split(datalist, 7)
    returndata = {
        "total": contributions,
        "contributions": datalistsplit
    }
    return returndata


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        result = parse.urlparse(path)
        query = parse.parse_qs(result.query).get("user", [])
        if not len(query) > 0:
            data = {"code": "400", "msg": "Invalid Parameter", "param": {"user": "str"}}
            self.send_response(400)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            # user = path.split('?')[1]
            data = getdata(query[0])
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        return


if __name__ == "__main__":
    host = ('localhost', 8080)
    server = HTTPServer(host, handler)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
