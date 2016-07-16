#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import subprocess
from pathlib import Path

def extract(rep):
    reppath = Path(rep)
    print("Extract data from the newest package")
    files = sorted(reppath.iterdir(), key=lambda x: x.stat().st_mtime)
    files.reverse()
    datapath = Path("/dev/shm/data")
    if datapath.exists():
        if not genpath.is_dir():
            print('/dev/shm/data is not a directory')
            exit(-1)
    else:
        datapath.mkdir(parents=True)
    subprocess.call(['tar', '-zxf', str(files[0]), '-C', '/dev/shm/data'])
    print("Done")

def main(rep):
    extract(rep)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Extract the package.')
    parser.add_argument('rep', action = 'store', help = 'Path of repository')
    args = parser.parse_args()
    main(args.rep)
