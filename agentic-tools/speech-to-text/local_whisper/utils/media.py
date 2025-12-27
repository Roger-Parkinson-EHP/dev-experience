"""Media control utilities for muting/unmuting system audio.

Uses Windows Core Audio API (pycaw) for explicit mute control instead of toggle.
"""

from local_whisper.utils.logger import get_logger

logger = get_logger(__name__)

# Track mute state so we only unmute if we muted
_muted_by_us = False
_was_muted_before = False
_audio_interface = None


def _get_audio_interface():
    """Get or create the Windows audio interface."""
    global _audio_interface
    if _audio_interface is None:
        try:
            from pycaw.pycaw import AudioUtilities

            speakers = AudioUtilities.GetSpeakers()
            _audio_interface = speakers.EndpointVolume
            logger.info("Audio interface initialized via pycaw")
        except ImportError:
            logger.warning("pycaw not installed - mute feature disabled. Run: pip install pycaw")
            return None
        except Exception as e:
            logger.warning(f"Failed to get audio interface: {e}")
            return None
    return _audio_interface


def mute_audio() -> None:
    """Mute system audio while recording."""
    global _muted_by_us, _was_muted_before

    interface = _get_audio_interface()
    if interface is None:
        logger.warning("No audio interface available for muting")
        return

    try:
        # Check if already muted - don't override user's setting
        _was_muted_before = bool(interface.GetMute())
        if _was_muted_before:
            logger.info("System already muted, skipping")
            return

        # Explicitly set mute to True
        interface.SetMute(True, None)
        _muted_by_us = True
        logger.info("System audio MUTED")
    except Exception as e:
        logger.error(f"Failed to mute audio: {e}")


def unmute_audio(force: bool = False) -> None:
    """Unmute system audio after recording.

    Args:
        force: If True, attempt to unmute even if we didn't mute
    """
    global _muted_by_us, _was_muted_before

    logger.info(f"unmute_audio called: _muted_by_us={_muted_by_us}, force={force}")

    interface = _get_audio_interface()
    if interface is None:
        logger.warning("No audio interface available for unmuting")
        _muted_by_us = False
        return

    if _muted_by_us or force:
        try:
            # Only unmute if we were the ones who muted
            if not _was_muted_before:
                interface.SetMute(False, None)
                logger.info("System audio UNMUTED")
            else:
                logger.info("System was already muted before, leaving muted")
            _muted_by_us = False
        except Exception as e:
            logger.error(f"Failed to unmute audio: {e}")
            _muted_by_us = False
    else:
        logger.info("unmute_audio: nothing to do (_muted_by_us=False)")


def force_unmute() -> None:
    """Force unmute - call this if audio seems stuck muted."""
    global _muted_by_us, _was_muted_before
    _was_muted_before = False  # Ignore previous state
    _muted_by_us = True
    unmute_audio()
