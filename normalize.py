import argparse

# Parser
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--links_path", type=str, default='2021-01-15_balouzza.json',
                    help="List of links in JSON or TXT format.")
parser.add_argument('-verbose', type=bool, default=True,
                    help="Verbosité")

opt = parser.parse_args()
if opt.verbose: print(opt)

import os
os.makedirs('output', exist_ok=True)
folder_name = opt.links_path.replace('.json', '').replace('.txt', '')
os.makedirs(f'output/{folder_name}', exist_ok=True)

print(50*'-')
print('# normalize')
print(50*'-')

import glob
import shutil
for fname in glob.glob(f'output/{folder_name}/*.opus'):
    cmd = f'ffmpeg -y -i "{fname}" -filter:a "dynaudnorm=p=0.9:s=5" /tmp/file.opus'
    if opt.verbose: print(cmd)
    os.system(cmd)
    cmd = f'shutil.move("/tmp/file.opus", "{fname}")'
    if opt.verbose: print(cmd)
    os.system(cmd)

