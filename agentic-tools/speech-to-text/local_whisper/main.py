"""Main entry point for WhisperFlow."""

import sys
import os
import argparse
import time

# Add parent directory to path for direct script execution
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from local_whisper.utils.logger import init_logger, get_logger, log_exception

# Initialize logger FIRST
init_logger()
logger = get_logger("whisperflow.main")


def kill_prior_instances() -> int:
    """Kill any prior WhisperFlow instances. Returns count of killed processes."""
    import subprocess
    killed = 0
    current_pid = os.getpid()

    try:
        # Use PowerShell to find and kill python processes with whisperflow in command line
        ps_script = '''
        Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
        Where-Object { $_.CommandLine -like '*whisperflow*' } |
        Select-Object -ExpandProperty ProcessId
        '''
        result = subprocess.run(
            ['powershell', '-Command', ps_script],
            capture_output=True, text=True, timeout=10
        )

        for line in result.stdout.strip().split('\n'):
            line = line.strip()
            if line.isdigit():
                pid = int(line)
                if pid != current_pid:
                    try:
                        subprocess.run(['taskkill', '/F', '/PID', str(pid)],
                                      capture_output=True, timeout=5)
                        killed += 1
                        logger.info(f"Killed prior instance (PID {pid})")
                    except Exception:
                        pass
    except Exception as e:
        logger.debug(f"Error checking for prior instances: {e}")

    return killed

from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QThread, pyqtSignal

from local_whisper.audio import AudioRecorder
from local_whisper.transcriber import Transcriber
from local_whisper.streaming_transcriber import StreamingTranscriber
from local_whisper.hotkey import HotkeyHandler
from local_whisper.utils.clipboard import copy_and_paste
from local_whisper.utils.config import get_config, save_config
from local_whisper.utils.media import mute_audio, unmute_audio
from local_whisper.ui.main_window import WhisperFlowWindow, AppState


class WhisperFlowApp:
    """Main application controller."""

    def __init__(self):
        logger.info("Initializing WhisperFlowApp")

        try:
            self.app = QApplication(sys.argv)
            self.app.setQuitOnLastWindowClosed(False)
            logger.debug("QApplication created")

            # Initialize components
            self.window = WhisperFlowWindow()
            logger.debug("Window created")

            self.recorder = AudioRecorder()
            logger.debug("AudioRecorder created")

            self.transcriber = Transcriber()
            logger.debug("Transcriber created")

            self.streaming_transcriber = StreamingTranscriber()
            logger.debug("StreamingTranscriber created")

            self.hotkey_handler = HotkeyHandler()
            logger.debug("HotkeyHandler created")

            # State
            self._is_recording = False
            self._last_transcript = ""  # Store last transcript for right-click paste

            # Set up callbacks
            self._setup_callbacks()
            logger.debug("Callbacks configured")

            # Set up system tray
            self._setup_tray()
            logger.debug("System tray configured")

            logger.info("WhisperFlowApp initialized successfully")

        except Exception as e:
            log_exception(logger, "Failed to initialize WhisperFlowApp", e)
            raise

    def _setup_callbacks(self) -> None:
        """Wire up component callbacks."""
        self.hotkey_handler.set_toggle_callback(self._on_hotkey_toggle)
        self.recorder.set_audio_level_callback(
            lambda level: self.window.update_audio_level(level)
        )
        self.transcriber.set_model_loaded_callback(self._on_model_loaded)
        self.streaming_transcriber.set_model_loaded_callback(self._on_model_loaded)
        self.streaming_transcriber.set_partial_result_callback(
            lambda text: self.window.update_live_text(text[-80:] if len(text) > 80 else text)
        )
        self.window.paste_last_requested.connect(self._on_paste_last_requested)
        self.window.device_change_requested.connect(self._on_device_change)
        self.window.toggle_mute_requested.connect(self._on_toggle_mute)
        self.window.toggle_auto_paste_requested.connect(self._on_toggle_auto_paste)

    def _on_toggle_mute(self, enabled: bool) -> None:
        """Toggle mute while recording setting."""
        config = get_config()
        config.pause_media_while_recording = enabled
        save_config()
        status = "enabled" if enabled else "disabled"
        logger.info(f"Mute while recording: {status}")
        self.window.status_label.setText(f"🔇 Mute: {status}")
        self.window.status_label.setVisible(True)
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(1500, lambda: self.window.set_state(AppState.IDLE))

    def _on_toggle_auto_paste(self, enabled: bool) -> None:
        """Toggle auto-paste setting."""
        config = get_config()
        config.auto_paste = enabled
        save_config()
        status = "enabled" if enabled else "disabled"
        logger.info(f"Auto-paste: {status}")
        self.window.status_label.setText(f"📋 Auto-paste: {status}")
        self.window.status_label.setVisible(True)
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(1500, lambda: self.window.set_state(AppState.IDLE))

    def _on_device_change(self, device_id) -> None:
        """Handle microphone device selection."""
        self.recorder.set_device(device_id)
        config = get_config()
        config.audio_device_id = device_id
        save_config()

        # Show confirmation
        if device_id is not None:
            import sounddevice as sd
            device_info = sd.query_devices(device_id)
            self.window.status_label.setText(f"🎤 {device_info['name'][:30]}")
        else:
            self.window.status_label.setText("🎤 System Default")
        self.window.status_label.setVisible(True)

        from PyQt6.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self.window.set_state(AppState.IDLE))

    def _on_paste_last_requested(self) -> None:
        """Handle right-click 'Paste Last Transcript' request."""
        from local_whisper.utils.clipboard import copy_to_clipboard
        if self._last_transcript:
            logger.info(f"Copying last transcript to clipboard: {len(self._last_transcript)} chars")
            copy_to_clipboard(self._last_transcript)
            # Show brief notification in the UI
            self.window.status_label.setText("📋 Copied to clipboard! Press Ctrl+V to paste")
            self.window.status_label.setVisible(True)
            # Hide after 2 seconds
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(2000, lambda: self.window.set_state(AppState.IDLE))
        else:
            logger.warning("No transcript available to copy")

    def _setup_tray(self) -> None:
        """Set up system tray icon."""
        self.tray = QSystemTrayIcon()
        self.tray.setToolTip("LocalWhisper")

        menu = QMenu()
        show_action = QAction("Show/Hide", menu)
        show_action.triggered.connect(self._toggle_window)
        menu.addAction(show_action)
        menu.addSeparator()
        quit_action = QAction("Quit", menu)
        quit_action.triggered.connect(self._quit)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
        self.tray.show()

    def _toggle_window(self) -> None:
        """Toggle window visibility."""
        if self.window.isVisible():
            self.window.hide()
            logger.debug("Window hidden")
        else:
            self.window.show()
            logger.debug("Window shown")

    def _quit(self) -> None:
        """Clean up and quit."""
        logger.info("Quitting LocalWhisper")
        self.hotkey_handler.stop()
        save_config()
        self.app.quit()

    def _on_hotkey_toggle(self) -> None:
        """Handle hotkey press - toggle recording."""
        logger.debug(f"Hotkey toggled, currently recording: {self._is_recording}")
        if self._is_recording:
            self._stop_recording()
        else:
            self._start_recording()

    def _start_recording(self) -> None:
        """Start recording audio."""
        try:
            if not self.streaming_transcriber.is_ready:
                logger.warning("Cannot start recording - model not ready")
                return

            logger.info("Starting recording")
            self._is_recording = True
            self._recording_start_time = time.time()

            # Mute system audio while recording
            config = get_config()
            if config.pause_media_while_recording:
                mute_audio()

            self.window.set_state(AppState.RECORDING)
            self.recorder.start_recording()
            logger.debug("Recording started successfully")

            # Start timeout timer (max 60 seconds recording)
            from PyQt6.QtCore import QTimer
            self._recording_timer = QTimer()
            self._recording_timer.setSingleShot(True)
            self._recording_timer.timeout.connect(self._on_recording_timeout)
            self._recording_timer.start(60000)  # 60 second max

            # Start streaming transcription
            self.streaming_transcriber.start_streaming()
            self.recorder.set_stream_chunk_callback(
                self.streaming_transcriber.add_audio
            )
            logger.debug("Streaming transcription started")

        except Exception as e:
            log_exception(logger, "Failed to start recording", e)
            self._is_recording = False
            self.window.set_state(AppState.IDLE)

    def _on_recording_timeout(self) -> None:
        """Handle recording timeout - auto-stop after max time."""
        if self._is_recording:
            logger.warning("Recording timeout - auto-stopping after 60 seconds")
            self._stop_recording()

    def _stop_recording(self) -> None:
        """Stop recording and transcribe."""
        try:
            if not self._is_recording:
                return

            # Cancel timers
            if hasattr(self, '_recording_timer') and self._recording_timer:
                self._recording_timer.stop()

            logger.info("Stopping recording")
            self._is_recording = False

            # Stop streaming callback
            self.recorder.set_stream_chunk_callback(None)

            # Unmute system audio
            config = get_config()
            if config.pause_media_while_recording:
                unmute_audio()

            self.window.set_state(AppState.PROCESSING)

            # Stop recorder and streaming transcriber
            self.recorder.stop_recording()
            final_text = self.streaming_transcriber.stop_streaming()
            logger.debug(f"Streaming transcription complete: {len(final_text)} chars")

            if final_text:
                self._on_transcription_done(final_text)
            else:
                logger.warning("No transcription result")
                self.window.set_state(AppState.IDLE)

        except Exception as e:
            log_exception(logger, "Failed to stop recording", e)
            self.window.set_state(AppState.IDLE)

    def _on_transcription_done(self, text: str) -> None:
        """Handle transcription result."""
        try:
            if text:
                # Calculate WPM
                recording_duration = time.time() - self._recording_start_time
                word_count = len(text.split())
                wpm = int((word_count / recording_duration) * 60) if recording_duration > 0 else 0

                logger.info(f"Transcription complete: '{text[:50]}...' ({len(text)} chars)")
                logger.info(f"Stats: {word_count} words in {recording_duration:.1f}s = {wpm} WPM")

                # Store for "Paste Last" feature
                self._last_transcript = text

                config = get_config()

                if config.show_preview:
                    self.window.show_text(text)

                if config.auto_paste:
                    logger.debug("Auto-pasting text")
                    success = copy_and_paste(text)
                    if success:
                        logger.info("Text pasted successfully")
                    else:
                        logger.error("Failed to paste text")
            else:
                logger.warning("Transcription returned empty text")
                self.window.set_state(AppState.IDLE)

        except Exception as e:
            log_exception(logger, "Error in transcription callback", e)
            self.window.set_state(AppState.IDLE)

    def _on_model_loaded(self) -> None:
        """Handle model loaded event."""
        logger.info("Whisper model loaded - ready to use!")
        self.window.set_state(AppState.IDLE)

    def run(self) -> int:
        """Run the application."""
        try:
            logger.info("Starting LocalWhisper")

            # Show window
            self.window.show()
            logger.debug("Window displayed")

            # Start loading model in background (streaming transcriber for real-time)
            self.window.set_state(AppState.LOADING)
            logger.info("Loading Whisper model in background...")
            self.streaming_transcriber.load_model_async()

            # Start hotkey listener
            self.hotkey_handler.start()

            config = get_config()
            logger.info(f"Hotkey: {config.hotkey}")
            logger.info("LocalWhisper ready!")

            # Run event loop
            return self.app.exec()

        except Exception as e:
            log_exception(logger, "Error running WhisperFlow", e)
            return 1


def run_self_test() -> bool:
    """Run automated self-test to verify all components work."""
    logger.info("=" * 60)
    logger.info("Running LocalWhisper Self-Test")
    logger.info("=" * 60)

    all_passed = True

    # Test 1: Config
    logger.info("Test 1: Configuration")
    try:
        config = get_config()
        logger.info(f"  Model: {config.model_size}")
        logger.info(f"  Hotkey: {config.hotkey}")
        logger.info(f"  Auto-paste: {config.auto_paste}")
        logger.info("  [PASS] Configuration loaded")
    except Exception as e:
        logger.error(f"  [FAIL] Configuration: {e}")
        all_passed = False

    # Test 2: Audio devices
    logger.info("Test 2: Audio Devices")
    try:
        from local_whisper.audio import AudioRecorder
        devices = AudioRecorder.get_input_devices()
        logger.info(f"  Found {len(devices)} input device(s)")
        for d in devices[:3]:  # Show first 3
            logger.info(f"    - {d['name']}")
        if devices:
            logger.info("  [PASS] Audio devices available")
        else:
            logger.warning("  [WARN] No audio input devices found")
    except Exception as e:
        logger.error(f"  [FAIL] Audio devices: {e}")
        all_passed = False

    # Test 3: Whisper model loading
    logger.info("Test 3: Whisper Model")
    try:
        from local_whisper.transcriber import Transcriber
        transcriber = Transcriber()
        logger.info("  Loading model (this may take a moment)...")
        transcriber.load_model("tiny")  # Use tiny for faster test
        if transcriber.is_ready:
            logger.info("  [PASS] Whisper model loaded")
        else:
            logger.error("  [FAIL] Model not ready after load")
            all_passed = False
    except Exception as e:
        logger.error(f"  [FAIL] Whisper model: {e}")
        all_passed = False

    # Test 4: Clipboard
    logger.info("Test 4: Clipboard")
    try:
        from local_whisper.utils.clipboard import copy_to_clipboard, get_clipboard_text
        test_text = "LocalWhisper test 12345"
        copy_to_clipboard(test_text)
        result = get_clipboard_text()
        if result == test_text:
            logger.info("  [PASS] Clipboard working")
        else:
            logger.error(f"  [FAIL] Clipboard mismatch: got '{result}'")
            all_passed = False
    except Exception as e:
        logger.error(f"  [FAIL] Clipboard: {e}")
        all_passed = False

    # Test 5: Hotkey registration
    logger.info("Test 5: Hotkey Registration")
    try:
        from local_whisper.hotkey import HotkeyHandler
        handler = HotkeyHandler()
        handler.set_toggle_callback(lambda: None)
        handler.start()
        if handler.is_enabled:
            logger.info("  [PASS] Hotkey registered")
            handler.stop()
        else:
            logger.error("  [FAIL] Hotkey not registered")
            all_passed = False
    except Exception as e:
        logger.error(f"  [FAIL] Hotkey: {e}")
        all_passed = False

    # Summary
    logger.info("=" * 60)
    if all_passed:
        logger.info("Self-Test PASSED - All components working!")
    else:
        logger.error("Self-Test FAILED - Some components have issues")
    logger.info("=" * 60)

    return all_passed


def exception_hook(exc_type, exc_value, exc_tb):
    """Global exception handler to log uncaught exceptions."""
    import traceback
    logger.critical("Uncaught exception!")
    logger.critical(f"Type: {exc_type.__name__}")
    logger.critical(f"Value: {exc_value}")
    logger.critical("Traceback:")
    for line in traceback.format_tb(exc_tb):
        for l in line.strip().split('\n'):
            logger.critical(f"  {l}")
    # Also print to stderr
    sys.__excepthook__(exc_type, exc_value, exc_tb)


def main() -> None:
    """Main entry point."""
    # Install global exception handler
    sys.excepthook = exception_hook

    parser = argparse.ArgumentParser(description="LocalWhisper - Local speech-to-text")
    parser.add_argument("--test", action="store_true", help="Run self-test")
    parser.add_argument("--log-level", default="DEBUG", help="Log level (DEBUG, INFO, WARNING, ERROR)")
    parser.add_argument("--no-kill", action="store_true", help="Don't kill prior instances")
    args = parser.parse_args()

    if args.test:
        success = run_self_test()
        sys.exit(0 if success else 1)

    # Kill prior instances before starting (prevents duplicates)
    if not args.no_kill:
        killed = kill_prior_instances()
        if killed > 0:
            logger.info(f"Killed {killed} prior instance(s)")
            time.sleep(0.5)  # Brief pause to ensure cleanup

    try:
        app = WhisperFlowApp()
        sys.exit(app.run())
    except Exception as e:
        log_exception(logger, "Fatal error", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
