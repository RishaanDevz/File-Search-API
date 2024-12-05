# File Search API

A Flask-based REST API that enables searching files in your Downloads directory through HTTP endpoints or a web interface. Access your files locally or through a public URL using Loophole tunneling.

## Live Demo
Try out the web interface at: https://hg2agr94wa.ac1.ai. (you have to start the server and tunnel with loophole, steps are below)

## Features

- Search files by name in Downloads directory
- Filter files by extension
- Get file metadata (name, path, size)
- Web interface for easy searching
- Automatic tunneling via Loophole for public access

## Prerequisites

- Python 3.7+
- Loophole CLI
- Flask

## Installation

1. Clone the repository:
```bash
git clone https://github.com/RishaanDevz/File-Search-API
cd File-Search-API
```

2. Install dependencies:
```bash
pip install flask
```
To install Loophole, download the CLI from https://loophole.cloud/download

3. Install Loophole CLI following instructions from their website

## Configuration

1. Open `app.py` and replace `insert-subdomain-here` with your desired Loophole subdomain:
```python
subprocess.run(["loophole", "http", "8000", "--hostname", "your-subdomain"])
```

## Usage

1. Start the server:
```bash
python app.py
```

2. Access the API endpoints:

**Search by filename:**
```
GET /search/<search_term>
```

Example response:
```json
{
    "search_term": "document",
    "results": [
        {
            "filename": "document.pdf",
            "path": "/Users/username/Downloads/document.pdf",
            "size": 1234567
        }
    ],
    "count": 1
}
```

**Search by extension:**
```
GET /files/<extension>
```

Example response:
```json
{
    "extension": "pdf",
    "results": [
        {
            "filename": "document.pdf",
            "path": "/Users/username/Downloads/document.pdf",
            "size": 1234567
        }
    ],
    "count": 1
}
```

## Web Interface

Access the user-friendly web interface at https://hg2agr94wa.ac1.ai to:
- Search files without using API endpoints directly
- View file listings with size information
- Filter by file extensions
- Access your files through an intuitive interface

## Security Considerations

- The API exposes file information from your Downloads directory
- Use with caution when exposing through Loophole
- Consider implementing authentication for production use

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Future Ideas

**System Integration**
- Run as a LaunchDaemon/Service for persistent availability
- Automatic startup on system boot
- System tray integration for easy access

**File Transfer & Notifications**
- Email integration for sending found files
- Discord bot integration for file delivery
- Push notifications for long-running searches
- Batch file operations (zip and send multiple files)

**Enhanced Features**
- Content-based search for text files
- File preview generation
- Search filters (date, size, type)
- Search history and favorites
- Configurable search locations beyond Downloads folder

Feel free to contribute to any of these features or suggest new ones!
