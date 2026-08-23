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


def normalize_files(path, fmt='opus', verbose=True):
    """Core normalization logic applied to all .fmt files in path."""
    if verbose:
        print(50 * '-')
        print('# normalize')
        print(50 * '-')

    files = glob.glob(f'{path}/*.{fmt}')
    for fname in files:
        tmpfile = f"/tmp/{os.path.basename(fname)}.tmp-norm.{fmt}"
        cmd = f'ffmpeg -hide_banner -y -i "{fname}" -filter:a "dynaudnorm=p=0.9:s=5" "{tmpfile}"'
        if verbose:
            print(cmd)
        os.system(cmd)
        shutil.move(tmpfile, fname)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, required=True,
                        help="Folder containing audio files to normalize")
    parser.add_argument("-f", "--format", type=str, default='opus',
                        help="Audio format (default: opus)")
    parser.add_argument('-v', '--verbose', action='store_true', default=True,
                        help="Enable verbose output")
    opt = parser.parse_args()

    normalize_files(opt.path, opt.format, opt.verbose)