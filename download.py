from __future__ import unicode_literals
import youtube_dl
import argparse

# Parser
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--links_path", type=str, default='links',
                    help="Chemin vers la liste des liens")
parser.add_argument("-f", "--format", type=str, default='mp3',
                    help="Type de format")
parser.add_argument("-q", "--quality", type=str, default='192',
                    help="Niveau de qualité")
opt = parser.parse_args()
print(opt)

# Read links list
# Lecture des seeds
with open(opt.links_path, "r") as file:
    links = file.read().splitlines()
    
    print(links)


ydl_opts = {
    'format': 'bestaudio',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': opt.format,
        'preferredquality': opt.quality,
    }],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(links) 
    info = ydl.extract_info(links[0], download=False)
    print(info.get('title', None))
    
