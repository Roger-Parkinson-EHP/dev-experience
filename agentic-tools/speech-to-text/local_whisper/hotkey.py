"""Global hotkey handler using keyboard library."""

import keyboard
from typing import Optional, Callable
import threading
import time

from local_whisper.utils.config import get_config
from local_whisper.utils.logger import get_logger, log_exception

logger = get_logger(__name__)


class HotkeyHandler:
    """Handles global hotkey detection for toggle recording."""

    def __init__(self):
        self._on_toggle: Optional[Callable[[], None]] = None
        self._hotkey_id: Optional[int] = None
        self._enabled = False
        self._last_trigger_time = 0.0
        self._debounce_ms = 200  # Debounce to prevent rapid toggling

    def set_toggle_callback(self, callback: Callable[[], None]) -> None:
        """Set the callback for when hotkey is pressed."""
        self._on_toggle = callback

    def _on_hotkey_pressed(self) -> None:
        """Internal callback for hotkey press with debouncing."""
        logger.debug("Hotkey pressed!")
        current_time = time.time() * 1000
        if current_time - self._last_trigger_time < self._debounce_ms:
            logger.debug("Debounced - ignoring")
            return

        self._last_trigger_time = current_time

        if self._on_toggle:
            logger.debug("Calling toggle callback")
            # Run callback in separate thread to avoid blocking keyboard hook
            threading.Thread(target=self._on_toggle).start()
        else:
            logger.warning("No toggle callback set!")

    def start(self) -> None:
        """Start listening for the hotkey."""
        if self._enabled:
            logger.debug("Hotkey already enabled")
            return

        config = get_config()
        hotkey = config.hotkey

        # Don't suppress - it causes keyboard input issues
        try:
            self._hotkey_id = keyboard.add_hotkey(
                hotkey,
                self._on_hotkey_pressed,
                suppress=False  # Changed: don't block other keyboard input
            )
            self._enabled = True
            logger.info(f"Hotkey '{hotkey}' registered successfully")
        except Exception as e:
            log_exception(logger, f"Failed to register hotkey '{hotkey}'", e)

    def stop(self) -> None:
        """Stop listening for the hotkey."""
        if not self._enabled:
            return

        if self._hotkey_id is not None:
            try:
                keyboard.remove_hotkey(self._hotkey_id)
            except Exception:
                pass
            self._hotkey_id = None

        self._enabled = False

    def update_hotkey(self, new_hotkey: str) -> None:
        """Update the hotkey binding."""
        was_enabled = self._enabled
        if was_enabled:
            self.stop()

        config = get_config()
        config.hotkey = new_hotkey

        if was_enabled:
            self.start()

    @property
    def is_enabled(self) -> bool:
        """Check if hotkey listener is active."""
        return self._enabled
