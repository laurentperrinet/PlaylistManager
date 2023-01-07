import argparse

# Parser
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--links_path", type=str, default='2021-01-15_balouzza.json',
                    help="List of links in JSON or TXT format.")
parser.add_argument("--prefix", type=str, default='PL',
                    help="Prefix for filenames")
parser.add_argument("-f", "--format", type=str, default='opus',
                    help="Coding format")
parser.add_argument("-q", "--quality", type=str, default='0', # zero for best
                    help="Quality level")
parser.add_argument('-verbose', type=bool, default=True,
                    help="Verbosité")

opt = parser.parse_args()
if opt.verbose: print(opt)

import json
import yt_dlp
# convert txt to json
if 'txt' in opt.links_path:
    with open(opt.links_path, "r") as file:
       line_list = file.readlines()
       line_list = [item.rstrip() for item in line_list]
    links = {}
    for line in line_list:
        with yt_dlp.YoutubeDL() as ydl:
            # if opt.verbose: print(ydl.extract_info(line, download=False))
            title = ydl.extract_info(line, download=False).get('title', 'no title')
        links[line] = title
    print(links)
    with open(opt.links_path.replace('txt', 'json'), "w") as file:
        json.dump(links, file,  indent=4)
    import sys
    sys.exit()

# Lecture des liens
if 'json' in opt.links_path:
    with open(opt.links_path, "r") as file:
       links = json.load(file)


if opt.verbose: print(links)
import os
os.makedirs('output', exist_ok=True)
folder_name = opt.links_path.replace('.json', '').replace('.txt', '')
os.makedirs(f'output/{folder_name}', exist_ok=True)

print(50*'-')
print('# loop to check all is there')
print(50*'-')
# infos = {} 
for url in links.keys():
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False).get('title', None)
        # infos[title] = info
        if opt.verbose:
            print(info)

# print(infos)

print(50*'-')
print('# do the actual stuff')
print(50*'-')
number = 1
for url in links.keys():
    if opt.verbose: print(url, links[url])

    ydl_opts = {
        'format': 'bestaudio/best',
        #'outtmpl': f'output/{folder_name}/{opt.prefix}-{number:03d}-%(title)s.%(ext)s',
        'outtmpl': f'output/{folder_name}/{opt.prefix}-{number:03d}-{links[url]}-%(title)s.%(ext)s',
        #'outtmpl': f'output/{folder_name}/%(autonumber)s-%({title})s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': opt.format,
            'preferredquality': opt.quality,
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    number += 1

print(50*'-')
print('# normalize')
print(50*'-')

import glob

for fname in glob.glob(f'output/{folder_name}/*.opus'):
    cmd = f'ffmpeg -i "{fname}" -filter:a "dynaudnorm=p=0.9:s=5" "{fname}"'
    print(cmd)
    os.system(cmd)


