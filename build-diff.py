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

def main(src, rep, gen):
    reppath = Path(rep)
    genpath = Path(gen)
    if not reppath.is_dir():
        print('rep need to be a directory')
        return
    if genpath.exists():
        if not genpath.is_dir():
            print('The path to save generated patchs need to be a directory')
            return
    else:
        genpath.mkdir(parents=True)
    srcpath = Path(src)
    if is_gzip(srcpath):
        with gzip.open(str(srcpath), 'rb') as fin:
            fsout = tempfile.NamedTemporaryFile(dir='/tmp', delete=False)
            srcpath = Path(fsout.name)
            fsout.write(fin.read())
            fsout.close()
            srcmd5 = md5(srcpath)
    else:
        srcmd5 = md5(srcpath)
    count = 0
    files = sorted(reppath.iterdir(), key=lambda x: x.stat().st_mtime)
    files.reverse()
    for x in files:
        if x.is_file():
            if count > 4:
                print('No need to build diff for old data package ' + x.name)
                continue
            fout = None
            if is_gzip(x):
                with gzip.open(str(x), 'rb') as fin:
                    fout = tempfile.NamedTemporaryFile(dir='/tmp', delete=False)
                    dstpath = Path(fout.name)
                    fout.write(fin.read())
                    fout.close()
                    xmd5 = md5(dstpath)
            else:
                xmd5 = md5(x)
                dstpath = x
            if srcmd5 != xmd5:
                print('Build diff between ' + src + ' and ' + str(x))
                subprocess.call(['bsdiff', str(dstpath), str(srcpath), '%s/%s-%s.patch' % (gen, srcmd5, xmd5)])
                count += 1
            if fout:
                os.unlink(fout.name)
    if fsout:
        os.unlink(fsout.name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'A tool to generate binary diff')
    parser.add_argument('-d', action = 'store', default='.', help = 'The path of generated patchs', dest = 'gen')
    parser.add_argument('src', action = 'store', help = 'The path of source binary file')
    parser.add_argument('rep', action = 'store', help = 'The path of repository directory')
    args = parser.parse_args()
    main(args.src, args.rep, args.gen)
