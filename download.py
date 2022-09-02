import youtube_dl
import argparse

# Parser
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--links_path", type=str, default='links.json',
                    help="List of links in JSON format.")
parser.add_argument("-f", "--format", type=str, default='opus',
                    help="Coding format")
parser.add_argument("-q", "--quality", type=str, default='192',
                    help="Quality level")
parser.add_argument('-verbose', type=bool, default=True,
                    help="Verbosité")

opt = parser.parse_args()
if opt.verbose: print(opt)


# TODO : alternate solution
# yt-dlp -o "%(autonumber)s-%(artist)s-%(track)s.%(ext)s" --extract-audio --audio-format mp3 --audio-quality 0 --ffmpeg-location /usr/bin/

# Lecture des liens
import json
with open(opt.links_path, "r") as file:
    links = json.load(file)
    if opt.verbose: print(links)

for link in links.keys():
    if opt.verbose: print(link, links[link])

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'output/{link}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': opt.format,
            'preferredquality': opt.quality,
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        if opt.verbose:
            info = ydl.extract_info(links[link], download=False)
            print(info.get('title', None))
        ydl.download([links[link]])
