"""Clipboard and paste utilities."""

import pyperclip
import pyautogui
import time
from typing import Optional


def copy_to_clipboard(text: str) -> bool:
    """Copy text to the system clipboard."""
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        print(f"Failed to copy to clipboard: {e}")
        return False


def paste_from_clipboard() -> bool:
    """Simulate Ctrl+Shift+V to paste from clipboard."""
    try:
        # Small delay to ensure clipboard is ready
        time.sleep(0.05)

        # Use Ctrl+Shift+V (works in terminals and most apps)
        pyautogui.hotkey('ctrl', 'shift', 'v')
        return True
    except Exception as e:
        print(f"Failed to paste: {e}")
        return False


def copy_and_paste(text: str) -> bool:
    """Copy text to clipboard and paste it at cursor position."""
    if not text:
        return False

    # Store current clipboard content to restore later (optional)
    # old_clipboard = pyperclip.paste()

    if copy_to_clipboard(text):
        # Small delay to ensure text is in clipboard
        time.sleep(0.05)
        return paste_from_clipboard()

    return False


def get_clipboard_text() -> Optional[str]:
    """Get the current text from clipboard."""
    try:
        return pyperclip.paste()
    except Exception as e:
        print(f"Failed to get clipboard: {e}")
        return None
