# PDF/EPUB to Audiobook Converter

A Flask web application that converts PDF and EPUB files into audiobooks using advanced Text-to-Speech technology.

## Features

- Upload PDF and EPUB files
- Convert text to natural-sounding speech
- Real-time progress tracking
- Automatic chapter detection
- Download converted audiobooks as MP3 files
- Clean and intuitive web interface

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- ffmpeg

### System Dependencies

#### MacOS
```bash
brew install ffmpeg espeak
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install ffmpeg espeak-ng
```

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/pdf-audiobook-converter.git
cd pdf-audiobook-converter
```

2. Create and activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application
```bash
python3 app.py
```

2. Open your web browser and go to:
```
http://localhost:5000
```

3. Upload a PDF or EPUB file
4. Wait for the conversion to complete
5. Download your audiobook

## Project Structure
```
pdf-audiobook-converter/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
├── LICENSE               # License file
├── README.md             # Project documentation
├── templates/            # HTML templates
│   └── index.html        # Main page template
├── static/               # Static files (CSS, JS)
├── uploads/              # Temporary upload directory
└── audiobooks/           # Output directory for audiobooks
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- Uses [Coqui TTS](https://github.com/coqui-ai/TTS) for text-to-speech conversion
- Built with [Flask](https://flask.palletsprojects.com/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)