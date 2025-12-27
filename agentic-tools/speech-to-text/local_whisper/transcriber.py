"""Whisper transcription module using faster-whisper."""

import numpy as np
from typing import Optional, Callable
import threading
from faster_whisper import WhisperModel

from local_whisper.utils.config import get_config
from local_whisper.utils.logger import get_logger, log_exception

logger = get_logger(__name__)


class Transcriber:
    """Transcribes audio using faster-whisper."""

    def __init__(self):
        self._model: Optional[WhisperModel] = None
        self._loading = False
        self._on_model_loaded: Optional[Callable[[], None]] = None

    def set_model_loaded_callback(self, callback: Callable[[], None]) -> None:
        """Set callback for when model is loaded."""
        self._on_model_loaded = callback

    def load_model(self, model_size: Optional[str] = None) -> None:
        """Load the Whisper model (blocking)."""
        if self._model is not None:
            return

        config = get_config()
        size = model_size or config.model_size

        # Use CPU with int8 for best performance without CUDA
        logger.info(f"Loading Whisper model '{size}'...")
        try:
            self._model = WhisperModel(
                size,
                device="cpu",
                compute_type="int8"
            )
            logger.info(f"Whisper model '{size}' loaded successfully (CPU mode)")
        except Exception as e:
            log_exception(logger, f"Failed to load Whisper model '{size}'", e)
            raise

        if self._on_model_loaded:
            self._on_model_loaded()

    def load_model_async(self, model_size: Optional[str] = None) -> None:
        """Load the Whisper model in a background thread."""
        if self._loading or self._model is not None:
            return

        self._loading = True
        thread = threading.Thread(target=self._load_model_thread, args=(model_size,))
        thread.start()

    def _load_model_thread(self, model_size: Optional[str]) -> None:
        """Background thread for loading model."""
        try:
            self.load_model(model_size)
        except Exception as e:
            print(f"Error loading model: {e}", flush=True)
            import traceback
            traceback.print_exc()
        finally:
            self._loading = False

    def transcribe(self, audio: np.ndarray, language: Optional[str] = None) -> str:
        """Transcribe audio to text."""
        if self._model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        if len(audio) == 0:
            return ""

        config = get_config()
        lang = language or config.language

        # Build initial_prompt from custom vocabulary for better recognition
        initial_prompt = None
        if config.custom_vocabulary:
            # Format: comma-separated words become a prompt hint
            words = [w.strip() for w in config.custom_vocabulary.split(",") if w.strip()]
            if words:
                initial_prompt = ", ".join(words)

        # Transcribe with optimized settings for speed
        segments, info = self._model.transcribe(
            audio,
            language=lang,
            beam_size=1,      # Much faster than beam_size=5
            best_of=1,        # Faster sampling
            vad_filter=True,  # Voice activity detection
            vad_parameters=dict(
                min_silence_duration_ms=300,  # Faster silence detection
                speech_pad_ms=100
            ),
            initial_prompt=initial_prompt,
            without_timestamps=True,       # Skip timestamp computation
            condition_on_previous_text=False  # Each chunk independent = faster
        )

        # Combine all segments
        text_parts = []
        for segment in segments:
            text_parts.append(segment.text.strip())

        return " ".join(text_parts)

    def transcribe_async(self, audio: np.ndarray,
                         callback: Callable[[str], None],
                         language: Optional[str] = None) -> None:
        """Transcribe audio in a background thread."""
        thread = threading.Thread(
            target=self._transcribe_thread,
            args=(audio, callback, language)
        )
        thread.start()

    def _transcribe_thread(self, audio: np.ndarray,
                           callback: Callable[[str], None],
                           language: Optional[str]) -> None:
        """Background thread for transcription."""
        try:
            logger.debug(f"Transcribing {len(audio)} samples...")
            text = self.transcribe(audio, language)
            logger.debug(f"Transcription complete: {len(text)} chars")
            callback(text)
        except Exception as e:
            log_exception(logger, "Transcription error", e)
            callback("")

    @property
    def is_ready(self) -> bool:
        """Check if model is loaded and ready."""
        return self._model is not None

    @property
    def is_loading(self) -> bool:
        """Check if model is currently loading."""
        return self._loading
