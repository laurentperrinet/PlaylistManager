# PlaylistManager

A two-step pipeline for downloading and normalizing audio from YouTube:
1. **Metadata Generation** – Resolves YouTube URLs or "Artist - Title" strings into a structured JSON mapping
2. **Media Download** – Downloads audio as Opus, applies metadata tags, and runs `ffmpeg` dynamic audio normalization

## Installation

### 1. System Dependencies
This tool requires `ffmpeg` to be installed in your system PATH for audio conversion and normalization.

- **macOS (Homebrew)**:
  ```bash
  brew install ffmpeg
  ```
- **Ubuntu/Debian**:
  ```bash
  sudo apt update && sudo apt install ffmpeg
  ```

### 2. Python Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U -r requirements.txt
```


## Usage

The tool works in two main steps:

### 1. Metadata Generation
Create a `.txt` file containing either YouTube URLs or "Artist - Title" search strings. Run the script to resolve these into a `.json` mapping.

```bash
python download.py -p my_playlist.txt
```
This generates `my_playlist.json`. You can edit this JSON file to correct titles before downloading.

### 2. Media Download & Processing
Run the script using the JSON file to download the audio, apply metadata, and normalize the volume.

```bash
python download.py -p my_playlist.json
```

> **Note**: Metadata tagging is only supported for `.opus` output format (default).

### Metadata Tags
The JSON filename (without extension) becomes the **album** and **album artist** tags for all tracks:
- `my_playlist.json` → `album=my_playlist`, `albumartist=my_playlist`
- Track number and total are auto-assigned based on JSON order

### Advanced Options
- **Custom Prefix**: Add a prefix to filenames (e.g., `python download.py -p list.json --prefix "Album1 "`).
- **Format**: Specify audio format (default is `opus`).
- **Help**: See all available options with `python download.py -h`.

## Project Structure
- `output/`: Contains downloaded media organized by playlist name.
- `download.py`: Main entry point for metadata generation and downloading.
- `normalize.py`: Standalone utility for volume normalization.
