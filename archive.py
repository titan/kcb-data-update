#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import gzip
import hashlib
import os
import subprocess
import tempfile
from pathlib import Path

def md5(s):
    m = hashlib.md5()
    with s.open('rb') as f:
        m.update(f.read())
    return m.hexdigest()

def is_gzip(s):
    with s.open('rb') as f:
        header = f.read(2)
        if header[0] == 0x1f and header[1] == 0x8b:
            return True
        else:
            return False

def main(src, dst):
    srcpath = Path(src)
    dstpath = Path(dst)
    if not dstpath.exists():
        print(dst + ' not exists')
        return
    if not dstpath.is_dir():
        print(dst + ' need to be a directory')
        return
    if not srcpath.exists():
        print(src + ' not exists')
        return
    if not srcpath.is_file():
        print(src + ' need to be a file')
        return
    if is_gzip(srcpath):
        with gzip.open(str(srcpath), 'rb') as fin:
            fsout = tempfile.NamedTemporaryFile(dir='/tmp', delete=False)
            fsout.write(fin.read())
            fsout.close()
            srcmd5 = md5(Path(fsout.name))
            path = str(srcpath)
            suffix = path[path.find('.'):]
            subprocess.call(['mv', src, '%s/%s%s' % (dst, srcmd5, suffix)])
            os.unlink(fsout.name)
    else:
        srcmd5 = md5(srcpath)
        subprocess.call(['mv', src, '%s/%s%s.gz' % (dst, srcmd5, srcpath.suffix)])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'A tool to archive data binary package')
    parser.add_argument('src', action = 'store', help = 'The path of source binary file')
    parser.add_argument('dst', action = 'store', help = 'The path of destination repository')
    args = parser.parse_args()
    main(args.src, args.dst)
