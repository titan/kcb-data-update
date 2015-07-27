#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import hashlib
import subprocess
from pathlib import Path

def md5(s):
    m = hashlib.md5()
    with s.open('rb') as f:
        m.update(f.read())
    return m.hexdigest()

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
    srcmd5 = md5(srcpath)
    subprocess.call(['mv', src, '%s/%s%s' % (dst, srcmd5, srcpath.suffix)])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'A tool to archive data binary package')
    parser.add_argument('src', action = 'store', help = 'The path of source binary file')
    parser.add_argument('dst', action = 'store', help = 'The path of destination repository')
    args = parser.parse_args()
    main(args.src, args.dst)
