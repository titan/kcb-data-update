#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import base64
import hashlib
import hmac
import time
import httplib2
import subprocess
from pathlib import Path

def md5(s):
    m = hashlib.md5()
    with s.open('rb') as f:
        m.update(f.read())
    return m.hexdigest()

def sign(appkey, src):
    return base64.b64encode(hmac.new(appkey.encode('ascii'), src.encode('ascii'), digestmod=hashlib.sha1).digest()).decode('ascii')

def main(appid, appkey, host, src, root, desc):
    srcmd5 = md5(Path(src))
    gmt = time.strftime('%a, %d %b %Y %H:%M:%S GMT')
    req = httplib2.Http(disable_ssl_certificate_validation=True)
    data = ('{"checksum":"%s","root":"%s","description":"%s"}' % (srcmd5, root, desc)).encode('utf-8')
    headers = {'Content-Type': 'application/json', 'Authorization': 'KCB %s:%s' % (appid, sign(appkey, 'POST\n\n\n%s\n/data' % (gmt))), 'Date': gmt}
    subprocess.call(['curl', '-k', '-v', 'https://%s/data' % host, '--data', data, '-H', 'Content-Type: application/json', '-H', 'Authorization: KCB %s:%s' % (appid, sign(appkey, 'POST\n\n\n%s\n/data' % (gmt))), '-H', 'Date: %s' % gmt])
    #resp, content = req.request('https://%s/data' % host, 'POST', data, headers)
    #print(resp)
    #for h, v in resp.getheaders():
    #    print('%s: %s' % (h, v))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'A tool to register data package')
    parser.add_argument('--desc', action = 'store', default='', help = 'The description about the data package')
    parser.add_argument('src', action = 'store', help = 'The path of source file')
    parser.add_argument('root', action = 'store', help = 'The root url to access the data package')
    parser.add_argument('--app-id', action = 'store', dest = 'appid', default = '986ffe12-658a-44c4-b43c-dbed5ae5d0bc', help = 'Application ID')
    parser.add_argument('--app-key', action = 'store', dest = 'appkey', default = 'tm+O/r5QR9LrVuZHFIpDHkCQIcDBXehv', help = 'Secure Key')
    parser.add_argument('--host', action = 'store', default = 'localhost:9000', help = 'Host(include port)')
    args = parser.parse_args()
    main(args.appid, args.appkey, args.host, args.src, args.root, args.desc)
