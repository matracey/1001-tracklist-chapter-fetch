# Tracklist Chapter Fetch

A command-line application for extracting tracklists from [1001tracklists.com](https://www.1001tracklists.com) and generating FFMETADATA files for adding chapter metadata to audio files.

## Features

- Extract tracklist information from any 1001tracklists.com URL
- Generate FFMETADATA chapter files compatible with FFmpeg
- Handle various timestamp formats
- Bypass anti-scraping protections with Scrapling's stealth capabilities
- Provide detailed error reporting and logging options

## Installation

### Prerequisites

- Python 3.12+
- PDM (Python Dependency Manager)

### Setup

1. Clone the repository:

   ```shell
   git clone https://github.com/username/tracklist-chapter-fetch.git
   cd tracklist-chapter-fetch
   ```

2. Install dependencies using PDM:

   ```shell
   pdm install
   ```

## Usage

### Basic Usage

   ```shell
pdm tracklist_chapter_fetch URL [OPTIONS]
```

Where `URL` is the 1001tracklists.com URL you want to extract the tracklist from.

### Options

```plaintext
-o, --output OUTPUT_FILE  Output file path (default: output.ffmetadata)
-q, --quiet               Suppress progress messages
-v, --verbose             Show detailed processing information
-h, --help                Show help message
```

### Example

```shell
pdm tracklist_chapter_fetch https://www.1001tracklists.com/tracklist/295f7nbt/steve-angello-an21-size-sound-system-055-2025-03-20.html -o my_chapters.ffmetadata
```

This will:

1. Download the tracklist from the specified URL using Scrapling's stealth capabilities
2. Extract track names, artists, and timestamps
3. Generate an FFMETADATA file with chapter markers
4. Save the file to `my_chapters.ffmetadata`

## Using with FFmpeg

To add chapter metadata to an audio file using the generated FFMETADATA file:

```shell
ffmpeg -i input_audio.mp3 -i output.ffmetadata -map_metadata 1 -codec copy output_with_chapters.mp3
```

## Development

### Technologies Used

- **Scrapling**: A high-performance, intelligent web scraping library that adapts to website changes and provides undetectable requests.
- **FFMPEG Metadata format**: Standard format for adding chapter metadata to audio files.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
