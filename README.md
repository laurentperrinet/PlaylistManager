# PlaylistManager

A simple scrapper for sharing audio on the interweb.

## usage

1. Add bookmarks from youtube music videos to the `links.txt` file,
2. issue `python download.py -p 2025-02_Paris.txt` to create a JSON file with titles,
3. edit `links.json` and issue  `python download.py -p 2025-02_Paris.json` to download the media.

A question? Ask for help: `python download.py -h`.

## dependencies

```
pip install yt_dlp mutagen
```

## TODO

- [x] normalize / equalize the gain of each song