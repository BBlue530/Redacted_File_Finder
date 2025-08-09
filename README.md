# Redacted File Finder

## Overview

This tool automates the process of:

- Scraping historical URLs from the Wayback Machine
- Filtering URLs with specific file extensions
- Checking for available archived snapshots
- Downloading accessible files
- Extracting metadata from various file types

It is intended for use in research, digital forensics, archival exploration, and cybersecurity investigations.

## Usage

1. Clone or download this repository.

2. Ensure Python 3 is installed and available in your system path.

3. Run the setup script to initialize a virtual environment and install dependencies:

   ```bash
   python Filefinder.py
   ```

4. When prompted, enter the domain you want to search:

   ```bash
   Enter Website: example.com
   ```

5. The tool will:
   - Retrieve all historical URLs for the domain
   - Filter by supported file types
   - Check availability via the Wayback Machine
   - Download valid archived files
   - Optionally begin metadata extraction

6. After download, the user is prompted to extract metadata from the downloaded files. A metadata report will be saved to `metadata.txt`.

## Supported File Types

The tool currently supports metadata extraction for:

- Microsoft Excel (`.xls`, `.xlsx`)
- Microsoft Word (`.doc`, `.docx`)
- PDF files (`.pdf`)
- JSON and CSV files
- SQLite database files (`.db`, `.sql`, `.backup`)
- ZIP archives
- Raw image files (`.img`)

Other types may be filtered for download but are not guaranteed to be processed.
