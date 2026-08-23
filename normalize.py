#!/usr/bin/env python
"""
Normalize the volume of a bunch of audio files using ffmpeg dynaudnorm.

Usage:
    python normalize.py -p output/my_playlist -f opus
"""

import argparse
import os
import glob
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str, required=True,
                    help="Folder containing audio files to normalize")
parser.add_argument("-f", "--format", type=str, default='opus',
                    help="Audio format (default: opus)")
parser.add_argument('-v', '--verbose', type=lambda x: x.lower() != 'false', default=True,
                    help="Enable verbose output (default: True, use -v False to disable)")

opt = parser.parse_args()

if opt.verbose:
    print(opt)

print(50 * '-')
print('# normalize')
print(50 * '-')

for fname in glob.glob(f'{opt.path}/*.{opt.format}'):
    tmpfile = f"/tmp/{os.path.basename(fname)}.tmp-norm.{opt.format}"
    cmd = f'ffmpeg -hide_banner -y -i "{fname}" -filter:a "dynaudnorm=p=0.9:s=5" "{tmpfile}"'
    if opt.verbose:
        print(cmd)
    os.system(cmd)
    shutil.move(tmpfile, fname)

