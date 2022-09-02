import argparse

# Parser
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--links_path", type=str, default='2021-01-15_balouzza.json',
                    help="List of links in JSON format.")
parser.add_argument("--prefix", type=str, default='PL',
                    help="Coding format")
parser.add_argument("-f", "--format", type=str, default='opus',
                    help="Coding format")
parser.add_argument("-q", "--quality", type=str, default='0', # zero for best
                    help="Quality level")
parser.add_argument('-verbose', type=bool, default=True,
                    help="Verbosité")

opt = parser.parse_args()
if opt.verbose: print(opt)

# Lecture des liens
import json
with open(opt.links_path, "r") as file:
    links = json.load(file)
    #if opt.verbose: print(links)

import os
os.makedirs('output', exist_ok=True)
folder_name = opt.links_path.strip('.json')
os.makedirs(f'output/{folder_name}', exist_ok=True)

import yt_dlp
print(50*'-')
print('# loop to check all is there')
print(50*'-')
for title in links.keys():
    with yt_dlp.YoutubeDL() as ydl:
        if opt.verbose:
            info = ydl.extract_info(links[title], download=False)
            print(info.get('title', None))

print(50*'-')
print('# do the actual stuff')
print(50*'-')
number = 1
for title in links.keys():
    if opt.verbose: print(title, links[title])

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'output/{folder_name}/{opt.prefix}-{number:03d}-{title}-%(title)s.%(ext)s',
        #'outtmpl': f'output/{folder_name}/%(autonumber)s-%({title})s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': opt.format,
            'preferredquality': opt.quality,
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([links[title]])

    number += 1
