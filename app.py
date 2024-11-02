# app.py
from pathlib import Path
import os
import threading
from queue import Queue
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import logging

from flask import Flask, request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
import fitz
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import torch
from TTS.api import TTS
import numpy as np
from pydub import AudioSegment
import soundfile as sf

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
class Config:
    UPLOAD_FOLDER = 'uploads'
    OUTPUT_FOLDER = 'audiobooks'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    CHUNK_SIZE = 300
    ALLOWED_EXTENSIONS = {'.pdf', '.epub'}
    TTS_MODELS = {
        'primary': "tts_models/en/ljspeech/glow-tts",
        'fallback': "tts_models/en/ljspeech/tacotron2-DDC"
    }

@dataclass
class ConversionJob:
    id: str
    input_path: str
    status: str = 'processing'
    progress: float = 0
    output_dir: Optional[str] = None
    error: Optional[str] = None

class TextExtractor:
    @staticmethod
    def from_pdf(pdf_path: str) -> str:
        try:
            text_parts = []
            with fitz.open(pdf_path) as pdf_doc:
                for page in pdf_doc:
                    text_parts.append(page.get_text())
            return "\n".join(text_parts)
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise

    @staticmethod
    def from_epub(epub_path: str) -> str:
        try:
            text_parts = []
            book = epub.read_epub(epub_path)
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    text_parts.append(soup.get_text())
            return "\n".join(text_parts)
        except Exception as e:
            logger.error(f"Error extracting text from EPUB: {e}")
            raise

class TextProcessor:
    @staticmethod
    def chunk_text(text: str, chunk_size: int = Config.CHUNK_SIZE) -> List[str]:
        sentences = text.replace('\n', ' ').split('.')
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            sentence = sentence + '.'
            sentence_size = len(sentence)
            
            if current_size + sentence_size > chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            current_chunk.append(sentence)
            current_size += sentence_size
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return [chunk for chunk in chunks if chunk.strip()]

class AudioConverter:
    def __init__(self):
        self.tts = self._initialize_tts()

    def _initialize_tts(self) -> Optional[TTS]:
        try:
            tts = TTS(
                model_name=Config.TTS_MODELS['primary'],
                progress_bar=False,
                gpu=torch.cuda.is_available()
            )
            logger.info("Successfully initialized primary TTS model")
            return tts
        except Exception as e:
            logger.error(f"Failed to load primary model: {e}")
            try:
                tts = TTS(
                    model_name=Config.TTS_MODELS['fallback'],
                    progress_bar=False,
                    gpu=torch.cuda.is_available()
                )
                logger.info("Successfully initialized fallback TTS model")
                return tts
            except Exception as e:
                logger.error(f"Failed to load fallback model: {e}")
                return None

    def convert_to_audio(self, text: str, output_path: str) -> bool:
        try:
            if not self.tts:
                raise Exception("TTS system not properly initialized")
            
            # Generate audio
            wav = self.tts.tts(text=text)
            
            # Save as WAV first
            wav_path = output_path.replace('.mp3', '.wav')
            sf.write(wav_path, wav, self.tts.synthesizer.output_sample_rate)
            
            # Convert WAV to MP3
            wav_audio = AudioSegment.from_wav(wav_path)
            wav_audio.export(output_path, format="mp3", parameters=["-q:a", "0"])
            
            # Cleanup
            os.remove(wav_path)
            return True
            
        except Exception as e:
            logger.error(f"Error in TTS conversion: {e}")
            return False

class AudiobookConverter:
    def __init__(self):
        self.audio_converter = AudioConverter()
        self.text_processor = TextProcessor()

    def process_book(self, job: ConversionJob) -> Optional[Path]:
        try:
            input_path = Path(job.input_path)
            output_dir = Path(Config.OUTPUT_FOLDER) / input_path.stem
            output_dir.mkdir(parents=True, exist_ok=True)

            # Extract text
            if input_path.suffix.lower() == '.pdf':
                text = TextExtractor.from_pdf(input_path)
            elif input_path.suffix.lower() == '.epub':
                text = TextExtractor.from_epub(input_path)
            else:
                raise ValueError("Unsupported file format")

            # Process chunks
            chunks = self.text_processor.chunk_text(text)
            if not chunks:
                raise Exception("No valid text chunks found to process")

            # Convert chunks to audio
            audio_segments = []
            for i, chunk in enumerate(chunks):
                job.progress = (i / len(chunks)) * 100
                
                chunk_path = output_dir / f"chunk_{i}.mp3"
                if self.audio_converter.convert_to_audio(chunk, str(chunk_path)):
                    try:
                        segment = AudioSegment.from_mp3(str(chunk_path))
                        audio_segments.append(segment)
                    except Exception as e:
                        logger.error(f"Error loading chunk {i}: {e}")
                    finally:
                        try:
                            os.remove(chunk_path)
                        except:
                            pass

            # Combine audio segments
            if audio_segments:
                final_path = output_dir / "audiobook.mp3"
                combined = audio_segments[0]
                for segment in audio_segments[1:]:
                    combined += segment
                combined.export(str(final_path), format='mp3', parameters=["-q:a", "0"])
                
                job.progress = 100
                job.status = 'completed'
                job.output_dir = str(output_dir)
                return output_dir
            
            raise Exception("No audio segments were successfully created")

        except Exception as e:
            logger.error(f"Error processing book: {e}")
            job.status = 'failed'
            job.error = str(e)
            raise

# Flask application setup
app = Flask(__name__)
app.config.from_object(Config)

# Ensure required directories exist
for folder in [Config.UPLOAD_FOLDER, Config.OUTPUT_FOLDER]:
    Path(folder).mkdir(exist_ok=True)

# Global state
conversion_jobs: Dict[str, ConversionJob] = {}
job_queue = Queue()
converter = AudiobookConverter()

def process_job(job_id: str) -> None:
    job = conversion_jobs[job_id]
    try:
        converter.process_book(job)
    except Exception as e:
        job.status = 'failed'
        job.error = str(e)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'No file selected'}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    job_id = str(len(conversion_jobs))
    job = ConversionJob(id=job_id, input_path=file_path)
    conversion_jobs[job_id] = job
    
    thread = threading.Thread(target=process_job, args=(job_id,))
    thread.start()
    
    return jsonify({
        'job_id': job_id,
        'message': 'Conversion started'
    })

@app.route('/status/<job_id>')
def get_status(job_id):
    job = conversion_jobs.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify({
        'status': job.status,
        'progress': job.progress,
        'error': job.error,
        'output_dir': job.output_dir
    })

@app.route('/download/<job_id>')
def download_result(job_id):
    job = conversion_jobs.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    if job.status != 'completed':
        return jsonify({'error': 'Job not completed'}), 400
    
    output_dir = Path(job.output_dir)
    audiobook_path = output_dir / "audiobook.mp3"
    
    if not audiobook_path.exists():
        return jsonify({'error': 'Audiobook file not found'}), 404
    
    return send_file(
        audiobook_path,
        as_attachment=True,
        download_name=f"{output_dir.name}.mp3"
    )

if __name__ == '__main__':
    app.run(debug=True)
    