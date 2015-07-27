#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import gzip
import hashlib
import qiniu
from pathlib import Path

def md5(s):
    m = hashlib.md5()
    with s.open('rb') as f:
        m.update(f.read())
    return m.hexdigest()

def md5sum(d):
    m = hashlib.md5()
    m.update(d)
    return m.hexdigest()

def is_gzip(s):
    with s.open('rb') as f:
        header = f.read(2)
        if header[0] == 0x1f and header[1] == 0x8b:
            return True
        else:
            return False

def upload(token, src, name, to_gzip, be_gzip):
    print('Uploading ' + str(src) + ' to ' + name)
    with src.open('rb') as f:
        if to_gzip and not be_gzip:
            content = gzip.compress(f.read(), compresslevel = 9)
        else:
            content = f.read()
        ret, info = qiniu.put_data(token, name, content)
        if ret is None:
            print(info)

def main(src, access, secret, bucket):
    q = qiniu.Auth(access, secret)
    token = q.upload_token(bucket)
    srcpath = Path(src)
    if srcpath.is_file():
        if is_gzip(srcpath):
            be_gzip = True
            with open(src, 'rb') as f:
                name = md5sum(gzip.decompress(f.read())) + srcpath.suffix
        else:
            be_gzip = False
            name = md5(srcpath) + srcpath.suffix + '.gz'
        upload(token, srcpath, name, True, be_gzip)
    elif srcpath.is_dir():
        for x in srcpath.iterdir():
            if x.is_file():
                upload(token, x, x.name, False,  False)
    else:
        print(src + ' needs do be a file or dir')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'A tool to upload data binary packages')
    parser.add_argument('src', action = 'store', help = 'The path of source binary file or directory')
    parser.add_argument('--access-key', action = 'store', help = 'The access key of qiniu', dest='access')
    parser.add_argument('--secret-key', action = 'store', help = 'The secret key of qiniu', dest='secret')
    parser.add_argument('--bucket', action = 'store', help = 'The name of bucket')
    args = parser.parse_args()
    main(args.src, args.access, args.secret, args.bucket)
