# -*- coding: UTF-8 -*-

import requests
from urllib import parse
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}
url = "https://yunhei.qimeng.fun/piliang.php"

def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


def getdata(qq_list_origin):
    # qq_list = ast.literal_eval(qq_list_origin)
    qq_list = qq_list_origin
    qq_list_str = ""
    for item in qq_list:
        qq_list_str = qq_list_str + item + "\n"
    prarm = {
        "submit": "查询",
        "qq": qq_list_str
    }
    result = requests.post(url=url, headers=headers, data=prarm).text
    container = result[result.find("---------查询结果---------") + 43: result.find("------------------------------") - 33]
    itemReg = re.compile(r"[√×]\d{3,15}([\u4e00-\u9fa5，。]{1,15}|未记录)")
    items = itemReg.findall(container)
    retDict = {}
    wantedList = []
    for index, qq in enumerate(qq_list):
        if items[index] == "未记录":
            pass
        else:
            retDict[qq] = items[index]
            wantedList.append(qq)
    retDict["Blocks"] = wantedList
    return retDict

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        result = parse.urlparse(path)
        query = parse.parse_qs(result.query).get("users", [])
        try:
            # user = path.split('?')[1]
            json_query = json.loads(query[0])
            users = json_query["users"]
            data = getdata(users)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        except:
            data = {"code": "400", "msg": "Invalid Parameter", "param": {"users": ["user1", "user2"]}, "return": {"Blocks": ["Wanted_qq"], "{QQ}": "Result"}}
            self.send_response(400)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))



if __name__ == "__main__":
    host = ('localhost', 8080)
    server = HTTPServer(host, handler)
    print("Listening http://localhost:8080")
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()
