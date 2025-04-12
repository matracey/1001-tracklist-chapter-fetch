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

## Development

### Technologies Used

- **Scrapling**: A high-performance, intelligent web scraping library that adapts to website changes and provides undetectable requests.
- **FFMPEG Metadata format**: Standard format for adding chapter metadata to audio files.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.
