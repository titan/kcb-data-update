#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import subprocess
import os
import hashlib
from pathlib import Path

def md5(s):
    m = hashlib.md5()
    with s.open('rb') as f:
        m.update(f.read())
    return m.hexdigest()

def package(src):
    print("Build package")
    os.chdir(src)
    srcpath = Path(src)
    cmd = ['tar', 'cf', '../source.tar']
    files = srcpath.iterdir()
    for f in files:
        cmd.append(f.name)
    subprocess.call(cmd)
    dstpath = Path('/dev/shm/source.tar')
    dstmd5 = md5(dstpath)
    subprocess.call(['gzip', '-9', '/dev/shm/source.tar'])
    subprocess.call(['cp', '/dev/shm/source.tar.gz', '/dev/shm/' + dstmd5 + '.tar.gz'])
    print("Done")

def main(rep):
    package(rep)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Build the package.')
    parser.add_argument('src', action = 'store', default = '/dev/shm/data', help = 'Path of /dev/shm/data')
    args = parser.parse_args()
    main(args.src)
