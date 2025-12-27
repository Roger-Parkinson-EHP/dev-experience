"""Audio recording module using sounddevice."""

import numpy as np
import sounddevice as sd
from typing import Optional, Callable
import threading
import queue

from local_whisper.utils.logger import get_logger, log_exception

logger = get_logger(__name__)


class AudioRecorder:
    """Records audio from the default input device."""

    SAMPLE_RATE = 16000  # Whisper expects 16kHz
    CHANNELS = 1
    DTYPE = np.float32

    def __init__(self, device_id: Optional[int] = None):
        self._recording = False
        self._audio_queue: queue.Queue = queue.Queue()
        self._audio_data: list = []
        self._stream: Optional[sd.InputStream] = None
        self._on_audio_level: Optional[Callable[[float], None]] = None
        self._on_stream_chunk: Optional[Callable[[np.ndarray], None]] = None
        self._device_id = device_id  # None = default device

    def set_device(self, device_id: Optional[int]) -> None:
        """Set the input device to use for recording."""
        self._device_id = device_id
        if device_id is not None:
            device_info = sd.query_devices(device_id)
            logger.info(f"Audio device set to: {device_info['name']}")
        else:
            logger.info("Audio device set to: System Default")

    def set_audio_level_callback(self, callback: Callable[[float], None]) -> None:
        """Set callback for audio level updates (for UI visualization)."""
        self._on_audio_level = callback

    def set_stream_chunk_callback(self, callback: Optional[Callable[[np.ndarray], None]]) -> None:
        """Set callback for streaming audio chunks (for real-time transcription)."""
        self._on_stream_chunk = callback

    def _audio_callback(self, indata: np.ndarray, frames: int,
                        time_info: dict, status: sd.CallbackFlags) -> None:
        """Callback for audio stream."""
        if status:
            logger.warning(f"Audio callback status: {status}")

        # Copy the data to avoid buffer issues
        audio_chunk = indata.copy().flatten()
        self._audio_queue.put(audio_chunk)

        # Calculate audio level for visualization
        if self._on_audio_level:
            level = np.abs(audio_chunk).mean()
            self._on_audio_level(float(level))

        # Send chunk to streaming transcriber if configured
        if self._on_stream_chunk:
            self._on_stream_chunk(audio_chunk)

    def start_recording(self) -> None:
        """Start recording audio."""
        if self._recording:
            logger.debug("Already recording, ignoring start request")
            return

        try:
            logger.debug("Starting audio recording")
            self._recording = True
            self._audio_data = []

            # Clear the queue
            while not self._audio_queue.empty():
                try:
                    self._audio_queue.get_nowait()
                except queue.Empty:
                    break

            # Start the audio stream (use selected device or default)
            self._stream = sd.InputStream(
                samplerate=self.SAMPLE_RATE,
                channels=self.CHANNELS,
                dtype=self.DTYPE,
                callback=self._audio_callback,
                blocksize=1024,
                device=self._device_id  # None = default device
            )
            self._stream.start()
            logger.debug("Audio stream started")

            # Start thread to collect audio data
            self._collector_thread = threading.Thread(target=self._collect_audio)
            self._collector_thread.start()
            logger.debug("Audio collector thread started")

        except Exception as e:
            log_exception(logger, "Failed to start recording", e)
            self._recording = False
            raise

    def _collect_audio(self) -> None:
        """Collect audio data from the queue."""
        while self._recording:
            try:
                chunk = self._audio_queue.get(timeout=0.1)
                self._audio_data.append(chunk)
            except queue.Empty:
                continue

    def stop_recording(self) -> np.ndarray:
        """Stop recording and return the audio data."""
        if not self._recording:
            return np.array([], dtype=self.DTYPE)

        self._recording = False

        # Stop the stream
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None

        # Wait for collector thread
        if hasattr(self, '_collector_thread'):
            self._collector_thread.join(timeout=1.0)

        # Drain remaining queue items
        while not self._audio_queue.empty():
            try:
                chunk = self._audio_queue.get_nowait()
                self._audio_data.append(chunk)
            except queue.Empty:
                break

        # Concatenate all audio data
        if self._audio_data:
            return np.concatenate(self._audio_data)
        return np.array([], dtype=self.DTYPE)

    @property
    def is_recording(self) -> bool:
        """Check if currently recording."""
        return self._recording

    @staticmethod
    def get_input_devices() -> list:
        """Get list of available input devices with their indices, filtered for duplicates."""
        devices = sd.query_devices()
        input_devices = []
        seen_names = set()

        for i, d in enumerate(devices):
            if d['max_input_channels'] > 0:
                # Filter duplicates by name (Windows often shows same device multiple times)
                name = d['name']
                if name not in seen_names:
                    seen_names.add(name)
                    device_info = dict(d)
                    device_info['index'] = i
                    input_devices.append(device_info)

        return input_devices
