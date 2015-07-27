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

def main(src, rep, gen):
    srcmd5 = md5(Path(src))
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
    count = 0
    for x in sorted(reppath.iterdir(), key=lambda x: x.stat().st_mtime):
        if x.is_file():
            if count > 5:
                print('No need to build diff for old data package' + x.name)
                continue
            xmd5 = md5(x)
            if srcmd5 != xmd5:
                print('Build diff between ' + src + ' and ' + str(x))
                subprocess.call(['bsdiff', str(x), src, '%s/%s-%s.patch' % (gen, srcmd5, xmd5)])
                count += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'A tool to generate binary diff')
    parser.add_argument('-d', action = 'store', default='.', help = 'The path of generated patchs', dest = 'gen')
    parser.add_argument('src', action = 'store', help = 'The path of source binary file')
    parser.add_argument('rep', action = 'store', help = 'The path of repository directory')
    args = parser.parse_args()
    main(args.src, args.rep, args.gen)
