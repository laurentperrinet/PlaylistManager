import argparse

# Parser
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", type=str, default='output/2021-01-15_balouzza',
                    help="Folder of OPUS music files.")
parser.add_argument('-verbose', type=bool, default=True,
                    help="Verbosité")

opt = parser.parse_args()
if opt.verbose: print(opt)

import os

print(50*'-')
print('# normalize')
print(50*'-')

import glob
import shutil
for fname in glob.glob(f'{opt.path}/*.opus'):
    cmd = f'ffmpeg -y -i "{fname}" -filter:a "dynaudnorm=p=0.9:s=5" /tmp/file.opus 2> /dev/null'
    if opt.verbose: print(cmd)
    os.system(cmd)
    shutil.move("/tmp/file.opus", "{fname}")

