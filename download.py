#!/usr/bin/env python
"""
Download and convert online videos to audio files with a two-step pipeline:
1. Text to JSON: Resolve URLs and titles.
2. JSON to Audio: Download, tag, and normalize.
"""

import argparse
import json
import os
import sys
import glob
import shutil
import yt_dlp
from youtube_search import YoutubeSearch
from mutagen.oggopus import OggOpus

def parse_arguments():
    """Handles CLI argument parsing and provides usage examples."""
    examples = (
        "Examples:\n"
        "  # Step 1: Generate metadata from a text file\n"
        "  python download.py -p playlist.txt\n\n"
        "  # Step 2: Download audio using the generated JSON\n"
        "  python download.py -p playlist.json\n\n"
        "  # Optional: Use a prefix and custom format\n"
        "  python download.py -p playlist.json --prefix \"MyAlbum \" -f mp3"
    )
    
    parser = argparse.ArgumentParser(
        description="YouTube to Audio Downloader & Normalizer",
        epilog=examples,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-p", "--links_path", type=str, required=True,
                        help="Path to the links file (.txt for generation, .json for download)")
    parser.add_argument("--prefix", type=str, default='',
                        help="Prefix for the resulting filenames")
    parser.add_argument("-f", "--format", type=str, default='opus',
                        help="Audio format (default: opus)")
    parser.add_argument("-q", "--quality", type=str, default='0', 
                        help="Quality level (0 for best)")
    parser.add_argument('-v', '--verbose', action='store_true', default=True,
                        help="Enable verbose output")
    
    return parser.parse_args()

def generate_metadata(links_path, verbose):
    """
    Reads a .txt file and creates a .json mapping of URLs to titles.
    Handles both direct URLs and 'Artist - Title' search strings.
    """
    print(f"--- Generating metadata from {links_path} ---")
    links = {}
    
    with open(links_path, "r") as file:
        lines = [line.rstrip() for line in file if line.strip()]

    for line in lines:
        if 'http' in line:
            # We have the URL, fetch the title from YouTube
            with yt_dlp.YoutubeDL() as ydl:
                title = ydl.extract_info(line, download=False).get('title', 'no title')
            links[line] = title
        else:
            # Search for the best match based on 'Artist - Title'
            results = YoutubeSearch(line, max_results=1).to_dict()
            if results:
                match = results[0]
                url = f'https://www.youtube.com/watch?v={match["id"]}'
                print(f"Found: {match['title']} for search: {line}")
                links[url] = line
            else:
                print(f"No match found for: {line}")

    json_path = links_path.replace('.txt', '.json')
    with open(json_path, "w") as file:
        json.dump(links, file, indent=4)
    
    print(f"Metadata saved to {json_path}")
    return json_path

def download_audio(links, folder_name, prefix, fmt, quality, verbose):
    """Downloads audio and writes it to the output directory."""
    print(f"--- Downloading audio to output/{folder_name} ---")
    os.makedirs(f'output/{folder_name}', exist_ok=True)
    
    total = len(links)
    for i, (url, title) in enumerate(links.items(), 1):
        fname = f'output/{folder_name}/{prefix}{i:03d}-{title}.{fmt}'
        
        if verbose:
            print(f"[{i}/{total}] Processing: {title}")

        if not os.path.isfile(fname):
            fname_strip = fname.replace(f'.{fmt}', '')
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': fname_strip,
                'metadata-from-title': "%(artist)s - %(title)s",
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': fmt,
                    'preferredquality': quality,
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        
        # Apply metadata tagging (Limited to OPUS as per mutagen.oggopus)
        if fmt == 'opus':
            try:
                audio = OggOpus(fname)
                # Expects "Artist - Title" format in the JSON value
                parts = title.split(' - ', 1)
                artist = parts[0] if len(parts) > 1 else "Unknown"
                song_title = parts[1] if len(parts) > 1 else parts[0]
                
                audio["title"] = song_title
                audio["albumartist"] = folder_name
                audio["album"] = folder_name
                audio["artist"] = artist
                audio["tracknumber"] = f"{i:03d}"
                audio["tracktotal"] = f"{total:03d}"
                audio.save()
            except Exception as e:
                print(f"Metadata error for {fname}: {e}")

def normalize_audio(folder_name, fmt):
    """Applies dynamic audio normalization using FFmpeg."""
    print(f"--- Normalizing audio in output/{folder_name} ---")
    files = glob.glob(f'output/{folder_name}/*.{fmt}')
    
    for i, fname in enumerate(files):
        tmpfile = f"output/{folder_name}/{i:03d}_tmp-norm.{fmt}"
        # dynaudnorm is used for dynamic range compression to equalize perceived volume
        cmd = f'ffmpeg -hide_banner -y -i "{fname}" -filter:a "dynaudnorm=p=0.9:s=5" "{tmpfile}"'
        os.system(cmd)
        shutil.move(tmpfile, fname)

def main():
    opt = parse_arguments()
    
    if opt.links_path.endswith('.txt'):
        generate_metadata(opt.links_path, opt.verbose)
        sys.exit(0)
    
    if opt.links_path.endswith('.json'):
        with open(opt.links_path, "r") as file:
            links = json.load(file)
        
        folder_name = os.path.splitext(os.path.basename(opt.links_path))[0]
        
        download_audio(links, folder_name, opt.prefix, opt.format, opt.quality, opt.verbose)
        
        if opt.format == 'opus':
            normalize_audio(folder_name, opt.format)
        else:
            print("Normalization is currently only implemented for .opus files.")
            
    else:
        print("Error: links_path must be a .txt or .json file.")
        sys.exit(1)

if __name__ == "__main__":
    main()
