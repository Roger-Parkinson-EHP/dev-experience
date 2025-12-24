"""Media control utilities for muting/unmuting system audio."""

import ctypes
from ctypes import wintypes
from whisperflow.utils.logger import get_logger

logger = get_logger(__name__)

# Track mute state so we only unmute if we muted
_muted_by_us = False
_previous_volume = None

# Windows API constants
APPCOMMAND_VOLUME_MUTE = 0x80000
APPCOMMAND_VOLUME_UP = 0xA0000
APPCOMMAND_VOLUME_DOWN = 0x90000
WM_APPCOMMAND = 0x319


def _send_volume_command(command: int) -> None:
    """Send a volume command using Windows API."""
    try:
        # Get foreground window handle
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        if hwnd == 0:
            hwnd = ctypes.windll.user32.GetDesktopWindow()

        # Send the command
        ctypes.windll.user32.SendMessageW(hwnd, WM_APPCOMMAND, 0, command)
    except Exception as e:
        logger.debug(f"Volume command failed: {e}")


def mute_audio() -> None:
    """Mute system audio while recording."""
    global _muted_by_us
    try:
        _send_volume_command(APPCOMMAND_VOLUME_MUTE)
        _muted_by_us = True
        logger.debug("System audio muted")
    except Exception as e:
        logger.debug(f"Failed to mute audio: {e}")


def unmute_audio(force: bool = False) -> None:
    """Unmute system audio after recording.

    Args:
        force: If True, attempt to unmute even if we didn't mute
    """
    global _muted_by_us
    if _muted_by_us or force:
        try:
            _send_volume_command(APPCOMMAND_VOLUME_MUTE)  # Toggle back
            _muted_by_us = False
            logger.debug("System audio unmuted")
        except Exception as e:
            logger.debug(f"Failed to unmute audio: {e}")
            _muted_by_us = False  # Reset state even on failure


def force_unmute() -> None:
    """Force unmute - call this if audio seems stuck muted."""
    global _muted_by_us
    _muted_by_us = True  # Pretend we muted so unmute will work
    unmute_audio()
