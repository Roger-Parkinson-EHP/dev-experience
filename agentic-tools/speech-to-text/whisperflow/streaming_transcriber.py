"""Streaming Whisper transcription - transcribes chunks as they arrive."""

import numpy as np
from typing import Optional, Callable, List
import threading
import queue
import time
from faster_whisper import WhisperModel

from whisperflow.utils.config import get_config
from whisperflow.utils.logger import get_logger, log_exception

logger = get_logger(__name__)


class StreamingTranscriber:
    """
    Streaming transcriber that processes audio chunks in real-time.

    Instead of waiting for all audio, this transcribes chunks as they arrive,
    so when recording stops, most audio is already transcribed.
    """

    # Process audio in chunks of this duration (seconds)
    CHUNK_DURATION = 3.0  # 3 seconds per chunk
    SAMPLE_RATE = 16000

    def __init__(self):
        self._model: Optional[WhisperModel] = None
        self._loading = False
        self._on_model_loaded: Optional[Callable[[], None]] = None

        # Streaming state
        self._is_streaming = False
        self._audio_buffer: List[np.ndarray] = []
        self._transcribed_text: List[str] = []
        self._chunk_queue: queue.Queue = queue.Queue()
        self._transcribe_thread: Optional[threading.Thread] = None
        self._on_partial_result: Optional[Callable[[str], None]] = None

        # Performance tracking
        self._chunks_processed = 0
        self._total_transcribe_time = 0.0

    def set_model_loaded_callback(self, callback: Callable[[], None]) -> None:
        """Set callback for when model is loaded."""
        self._on_model_loaded = callback

    def set_partial_result_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for partial transcription results (for live preview)."""
        self._on_partial_result = callback

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
                compute_type="int8",
                num_workers=2  # Parallel processing
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

    def start_streaming(self) -> None:
        """Start streaming transcription mode."""
        if self._is_streaming:
            return

        logger.debug("Starting streaming transcription")
        self._is_streaming = True
        self._audio_buffer = []
        self._transcribed_text = []
        self._chunks_processed = 0
        self._total_transcribe_time = 0.0

        # Clear the queue
        while not self._chunk_queue.empty():
            try:
                self._chunk_queue.get_nowait()
            except queue.Empty:
                break

        # Start transcription worker thread
        self._transcribe_thread = threading.Thread(target=self._transcription_worker)
        self._transcribe_thread.start()

    def add_audio(self, audio_chunk: np.ndarray) -> None:
        """Add audio chunk to the buffer. Will auto-transcribe when enough audio."""
        if not self._is_streaming:
            return

        self._audio_buffer.append(audio_chunk)

        # Calculate total buffered audio duration
        total_samples = sum(len(chunk) for chunk in self._audio_buffer)
        duration = total_samples / self.SAMPLE_RATE

        # If we have enough audio, queue it for transcription
        if duration >= self.CHUNK_DURATION:
            audio = np.concatenate(self._audio_buffer)
            self._audio_buffer = []
            self._chunk_queue.put(audio)
            logger.debug(f"Queued {duration:.1f}s audio chunk for transcription")

    def _transcription_worker(self) -> None:
        """Background worker that transcribes queued audio chunks."""
        config = get_config()
        lang = config.language

        # Build initial_prompt from custom vocabulary
        initial_prompt = None
        if config.custom_vocabulary:
            words = [w.strip() for w in config.custom_vocabulary.split(",") if w.strip()]
            if words:
                initial_prompt = ", ".join(words)

        while self._is_streaming or not self._chunk_queue.empty():
            try:
                audio = self._chunk_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            if self._model is None:
                continue

            start_time = time.time()

            try:
                # Balanced transcription settings - accuracy + speed
                segments, info = self._model.transcribe(
                    audio,
                    language=lang,
                    beam_size=3,  # Better accuracy than 1, still fast
                    best_of=2,    # Consider 2 candidates
                    vad_filter=True,
                    vad_parameters=dict(
                        min_silence_duration_ms=300,
                        speech_pad_ms=100
                    ),
                    initial_prompt=initial_prompt,
                    without_timestamps=True,  # Skip timestamp computation
                    condition_on_previous_text=False  # Each chunk independent
                )

                # Collect text
                text_parts = []
                for segment in segments:
                    text_parts.append(segment.text.strip())

                chunk_text = " ".join(text_parts)
                if chunk_text:
                    self._transcribed_text.append(chunk_text)

                    # Notify of partial result
                    if self._on_partial_result:
                        full_text = " ".join(self._transcribed_text)
                        self._on_partial_result(full_text)

                elapsed = time.time() - start_time
                self._total_transcribe_time += elapsed
                self._chunks_processed += 1

                audio_duration = len(audio) / self.SAMPLE_RATE
                rtf = elapsed / audio_duration  # Real-time factor
                logger.debug(f"Chunk transcribed in {elapsed:.2f}s (RTF: {rtf:.2f}x)")

            except Exception as e:
                log_exception(logger, "Streaming transcription error", e)

    def stop_streaming(self) -> str:
        """Stop streaming and return final transcription."""
        if not self._is_streaming:
            return ""

        # Process any remaining audio in buffer
        if self._audio_buffer:
            audio = np.concatenate(self._audio_buffer)
            if len(audio) > self.SAMPLE_RATE * 0.5:  # Only if > 0.5 seconds
                self._chunk_queue.put(audio)
            self._audio_buffer = []

        # Signal stop and wait for worker
        self._is_streaming = False

        if self._transcribe_thread:
            self._transcribe_thread.join(timeout=5.0)
            self._transcribe_thread = None

        # Log performance stats
        if self._chunks_processed > 0:
            avg_time = self._total_transcribe_time / self._chunks_processed
            logger.info(f"Streaming complete: {self._chunks_processed} chunks, "
                       f"avg {avg_time:.2f}s per chunk")

        return " ".join(self._transcribed_text)

    def transcribe(self, audio: np.ndarray, language: Optional[str] = None) -> str:
        """Fallback: transcribe audio (batch mode, for compatibility)."""
        if self._model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        if len(audio) == 0:
            return ""

        config = get_config()
        lang = language or config.language

        initial_prompt = None
        if config.custom_vocabulary:
            words = [w.strip() for w in config.custom_vocabulary.split(",") if w.strip()]
            if words:
                initial_prompt = ", ".join(words)

        segments, info = self._model.transcribe(
            audio,
            language=lang,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(
                min_silence_duration_ms=500,
                speech_pad_ms=200
            ),
            initial_prompt=initial_prompt
        )

        text_parts = []
        for segment in segments:
            text_parts.append(segment.text.strip())

        return " ".join(text_parts)

    @property
    def is_ready(self) -> bool:
        """Check if model is loaded and ready."""
        return self._model is not None

    @property
    def is_loading(self) -> bool:
        """Check if model is currently loading."""
        return self._loading

    @property
    def is_streaming(self) -> bool:
        """Check if currently in streaming mode."""
        return self._is_streaming
