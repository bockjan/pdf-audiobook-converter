# PDF/EPUB to Audiobook Converter

A modern Flask web application that converts PDF and EPUB files into audiobooks using advanced Text-to-Speech technology. Features a sleek, dark-mode interface and a full-featured audio player.

## Features

### Conversion
- Upload PDF and EPUB files via drag-and-drop or file selection
- Real-time file information display
- Conversion progress tracking
- Support for large documents through chunk processing
- High-quality text-to-speech conversion

### Audio Player
- Full-featured audio controls:
  - Play/Pause
  - Forward/Backward 15 seconds
  - Adjustable playback speed (0.75x to 2x)
  - Volume control
  - Progress bar with seek functionality
  - Time display
- Keyboard shortcuts:
  - Space: Play/Pause
  - Left Arrow: Backward 15 seconds
  - Right Arrow: Forward 15 seconds
- Persistent user preferences:
  - Volume settings
  - Playback speed
  
### Interface
- Modern dark mode design
- Responsive layout
- Real-time progress tracking
- File information display
- Drag and drop support
- Interactive upload area
- Loading states and error handling

## Prerequisites

### System Requirements
- Python 3.11 or higher
- pip (Python package manager)
- ffmpeg (for audio processing)
- espeak (for text-to-speech)

### Installation on Different Systems

#### MacOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
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

3. Install Python dependencies
```bash
pip install -r requirements.txt
```

## Project Structure
```
pdf-audiobook-converter/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── .gitignore            # Git ignore file
├── LICENSE               # License file
├── README.md             # Project documentation
├── templates/            # HTML templates
│   └── index.html        # Main page template
├── static/               # Static files (CSS, JS)
├── uploads/              # Temporary upload directory
└── audiobooks/           # Output directory for audiobooks
```

## Dependencies

### Python Packages
- Flask: Web framework
- PyMuPDF: PDF processing
- EbookLib: EPUB processing
- TTS: Text-to-speech conversion
- pydub: Audio processing
- numpy: Numerical processing
- torch: Machine learning backend
- soundfile: Audio file handling

### Frontend
- Tailwind CSS: Styling
- Axios: HTTP client
- Inter font: Typography

## Usage

1. Start the application
```bash
python3 app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Upload a PDF or EPUB file:
   - Drag and drop the file, or
   - Click to select a file
   - File information will be displayed

4. Click "Convert to Audiobook"
   - Progress will be shown in real-time
   - Wait for conversion to complete

5. Use the audio player:
   - Play/Pause the audiobook
   - Adjust playback speed
   - Skip forward/backward
   - Control volume
   - Use keyboard shortcuts

## Contributing

1. Fork the repository
2. Create a feature branch
```bash
git checkout -b feature/YourFeatureName
```
3. Commit your changes
```bash
git commit -m 'Add some feature'
```
4. Push to the branch
```bash
git push origin feature/YourFeatureName
```
5. Create a Pull Request

## Future Enhancements
- Multiple voice options
- Chapter navigation
- Bookmarking feature
- Dark/Light theme toggle
- Mobile app version
- Batch processing
- Cloud storage integration

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgments

- Uses [Coqui TTS](https://github.com/coqui-ai/TTS) for text-to-speech conversion
- Built with [Flask](https://flask.palletsprojects.com/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)
- Audio processing with [pydub](https://github.com/jiaaro/pydub)