# Tracklist Chapter Fetch

A command-line application for extracting tracklists from 1001tracklists.com and generating FFMETADATA files for adding chapter metadata to audio files.

Technologies used:

- Python (3.9+)
- PDM (Package and dependency management)
- Scrapling (Web scraping library)
- FFMPEG Metadata format

## Python / CLI / Web Scraping Best Practices

This guide outlines **best practices** for building a **Python command-line application** with web scraping capabilities. The goal is to maintain **code clarity and maintainability** while providing robust error handling and a user-friendly interface.

### 📁 Project Structure

Follow a **clean and modular** folder structure:

```plaintext
/
  /src
    /tracklist_chapter_fetch     # Main package
      __init__.py                # Package initialization
      cli.py                     # Command-line interface
      scraper.py                 # Tracklist scraping functionality
      metadata.py                # FFMETADATA generation
      utils.py                   # Helper utilities
  /tests                         # Test files
  pyproject.toml                 # PDM project configuration
  README.md                      # Project documentation
  .gitignore                     # Git ignore file
  LICENSE                        # License information
```

📌 **Rules:**

- **Maintain separation of concerns**: Split functionality into logical modules
- **Use clear, descriptive naming** for files, functions, and variables
- **Document public interfaces** with docstrings
- **Only use PDM** for managing dependencies and packaging with the `pdm add` command, not `pip` or any other package manager.
- **Use `pdm run`** to execute scripts to ensure the correct environment is used
- **Use `pdm test`** to run tests to ensure the correct environment is used

### 🛠️ Coding Standards

#### Function Structure

- Keep functions **focused on a single task**
- Use **descriptive function names** (verb_noun)
- Add **type hints** to function parameters and return values
- Include **docstrings** for all public functions using Google style

```python
def parse_tracklist(html_content: str) -> list[dict]:
    """
    Extract tracks from 1001tracklists HTML content.
    
    Args:
        html_content: Raw HTML content from the tracklist page
        
    Returns:
        List of track dictionaries with 'artist', 'title', and 'timestamp' fields
    """
    # Implementation...
```

#### Error Handling

- Use **specific exceptions** when possible
- **Handle exceptions gracefully** with user-friendly messages
- Implement **logging** for debugging information

```python
try:
    tracklist = parse_tracklist(html_content)
except ParsingError as e:
    logger.error("Failed to parse tracklist: %s", str(e))
    sys.exit(1)
```

#### Command-line Interface

- Provide **clear help messages** and documentation
- Support **verbose output modes** for debugging
- Use **consistent option naming** (--output, --verbose, etc.)

### Web scraping guidelines

- Use **Scrapling** for web scraping
- Prefer the **Scrapling** library's built-in APIs to minimize boilerplate code
- Attempt to choose selectors that are both precise and resilient to website changes as 1001tracklists.com updates its HTML structure.
- Prioritize Unique Identifiers
- Utilize Class Names and Attributes
- Minimize Selector Complexity
- Test Across Multiple Pages
- Avoid Structural Selectors

### Tracklist Fetching

- Implement **rate limiting** to avoid overwhelming the server
- Handle **HTTP errors** and **timeouts** gracefully
- Refer to this example expected output of an extracted tracklist for [Steve Angello & AN21 - Size Sound System 055 2025-03-20](https://www.1001tracklists.com/tracklist/295f7nbt/steve-angello-an21-size-sound-system-055-2025-03-20.html)

```plaintext
;FFMETADATA1
[CHAPTER]
TIMEBASE=1/1000
START=34000
END=233000
title=Still Young & Brømance - Do It Again
[CHAPTER]
TIMEBASE=1/1000
START=233000
END=462000
title=Magnificence & Corey James ft. Rion S - Time Machine
[CHAPTER]
TIMEBASE=1/1000
START=462000
END=756000
title=Steve Angello & AN21 - Valodja (Liva K Remix)
[CHAPTER]
TIMEBASE=1/1000
START=756000
END=1011000
title=Steve Angello & Modern Tales - Darkness In Me
[CHAPTER]
TIMEBASE=1/1000
START=1011000
END=1188000
title=Steve Angello - Tivoli (KREAM Remix)
[CHAPTER]
TIMEBASE=1/1000
START=1188000
END=1363000
title=Deniz Koyu & WILL K - Into Sound
[CHAPTER]
TIMEBASE=1/1000
START=1363000
END=1584000
title=Catz 'N Dogz & Nala - Dance!
[CHAPTER]
TIMEBASE=1/1000
START=1584000
END=1776000
title=Loosie Grind - I Like
[CHAPTER]
TIMEBASE=1/1000
START=1776000
END=1909000
title=Keys N Krates x Pat Lok - Samba Surprise
[CHAPTER]
TIMEBASE=1/1000
START=1909000
END=2153000
title=Loco Dice feat. Haftbefehl - Ice Cold Dealer
[CHAPTER]
TIMEBASE=1/1000
START=2153000
END=2376000
title=PARISI - Feel It For You
[CHAPTER]
TIMEBASE=1/1000
START=2376000
END=2615000
title=Hugo Bordedebat - Feed My Soul
[CHAPTER]
TIMEBASE=1/1000
START=2615000
END=2793000
title=Lezolut - Space And Time
[CHAPTER]
TIMEBASE=1/1000
START=2793000
END=3095000
title=Kommando & Silhouette - NEW DAY (Vantrx Remix)
[CHAPTER]
TIMEBASE=1/1000
START=3095000
END=3334000
title=K-Ban & Nyky - As One
[CHAPTER]
TIMEBASE=1/1000
START=3334000
END=3533000
title=Nick Endhem - Fall Apart
```

### 🧪 Testing

- Write **unit tests** for core functionality
- Use **fixtures** for common test data
- Mock external dependencies (HTTP requests)

### 📦 Dependencies

Use PDM for dependency management:

- Keep dependencies **minimal and focused**
- Specify **version constraints** in pyproject.toml
- Document external dependencies in README

### 🔄 Development Workflow

1. Use PDM for dependency management and packaging
2. Follow a test-driven development approach
3. Document significant code changes
4. Keep commits focused and descriptive

### 🌟 Key Goals

- **Reliability**: Handle edge cases and network issues gracefully
- **Performance**: Minimize unnecessary HTTP requests
- **Maintainability**: Keep code clean, documented, and testable
- **User Experience**: Provide clear feedback and error messages
