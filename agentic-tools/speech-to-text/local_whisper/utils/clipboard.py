"""Clipboard and paste utilities."""

import pyperclip
import time
from typing import Optional

from local_whisper.utils.logger import get_logger

logger = get_logger(__name__)

# Track if paste is in progress to prevent double-paste
_paste_in_progress = False


def copy_to_clipboard(text: str) -> bool:
    """Copy text to the system clipboard."""
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        logger.error(f"Failed to copy to clipboard: {e}")
        return False


def paste_from_clipboard() -> bool:
    """Simulate Ctrl+V to paste from clipboard.

    Uses keyboard library for consistency with hotkey handling.
    Waits for modifier keys to be released before pasting.
    """
    global _paste_in_progress

    if _paste_in_progress:
        logger.debug("Paste already in progress, skipping")
        return False

    try:
        import keyboard

        _paste_in_progress = True

        # Wait for all modifier keys to be released (prevents double-paste from hotkey)
        max_wait = 1.0  # Max 1 second wait
        waited = 0
        while waited < max_wait:
            modifiers_pressed = (
                keyboard.is_pressed('ctrl') or
                keyboard.is_pressed('shift') or
                keyboard.is_pressed('alt')
            )
            if not modifiers_pressed:
                break
            time.sleep(0.05)
            waited += 0.05

        if waited >= max_wait:
            logger.warning("Timed out waiting for modifier keys to release")

        # Additional delay to ensure clean state
        time.sleep(0.1)

        # Use standard Ctrl+V (works in most apps, including terminals)
        keyboard.press_and_release('ctrl+v')

        logger.debug("Paste command sent")
        return True

    except Exception as e:
        logger.error(f"Failed to paste: {e}")
        return False
    finally:
        # Small delay before allowing next paste
        time.sleep(0.1)
        _paste_in_progress = False


def copy_and_paste(text: str) -> bool:
    """Copy text to clipboard and paste it at cursor position."""
    if not text:
        return False

    if copy_to_clipboard(text):
        # Delay to ensure clipboard is ready
        time.sleep(0.1)
        return paste_from_clipboard()

    return False


def get_clipboard_text() -> Optional[str]:
    """Get the current text from clipboard."""
    try:
        return pyperclip.paste()
    except Exception as e:
        logger.error(f"Failed to get clipboard: {e}")
        return None
