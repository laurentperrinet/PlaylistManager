# AGENTS.md - PlaylistManager

## Core Workflow
The tool processes audio downloads in a two-step pipeline:
1. **Metadata Generation**: `python download.py -p <name>.txt`
   - Reads `.txt` files containing YouTube URLs or "Artist - Title" strings.
   - Generates a corresponding `<name>.json` file mapping URLs to titles.
2. **Media Download**: `python download.py -p <name>.json`
   - Downloads audio using `yt-dlp` into `output/<name>/`.
   - Sets OggOpus metadata and applies `ffmpeg` dynamic audio normalization.

## Developer Commands
- **Dependencies**: `pip install -U -r requirements.txt`
- **Help**: `python download.py -h`
- **Standalone Normalization**: `python normalize.py -p output/<folder>` (Uses `ffmpeg` dynaudnorm).

## Key Constraints & Quirks
- **FFmpeg Dependency**: Both `download.py` and `normalize.py` rely on `ffmpeg` being installed in the system PATH.
- **Format Limit**: Metadata tagging (`mutagen.oggopus`) is explicitly implemented only for `.opus` files.
- **Output Structure**: Media is always stored in `output/` using the filename of the source JSON/TXT as the subfolder.
