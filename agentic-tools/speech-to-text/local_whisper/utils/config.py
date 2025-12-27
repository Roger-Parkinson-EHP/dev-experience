"""Configuration management for WhisperFlow."""

import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    """WhisperFlow configuration."""

    model_size: str = "base"  # tiny, base, small, medium, large
    hotkey: str = "ctrl+shift+space"  # Changed from alt+space to avoid conflicts
    auto_paste: bool = True
    language: str = "en"
    show_preview: bool = True
    preview_duration_ms: int = 1000
    audio_device_id: Optional[int] = None  # None = system default
    pause_media_while_recording: bool = True  # Pause music during recording
    custom_vocabulary: str = ""  # Comma-separated custom words for Whisper's initial_prompt

    @classmethod
    def get_config_path(cls) -> Path:
        """Get the path to the config file."""
        config_dir = Path.home() / ".whisperflow"
        config_dir.mkdir(exist_ok=True)
        return config_dir / "config.json"

    @classmethod
    def load(cls) -> "Config":
        """Load config from file or create default."""
        config_path = cls.get_config_path()
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    data = json.load(f)
                return cls(**data)
            except (json.JSONDecodeError, TypeError):
                pass
        return cls()

    def save(self) -> None:
        """Save config to file."""
        config_path = self.get_config_path()
        with open(config_path, "w") as f:
            json.dump(asdict(self), f, indent=2)


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global config instance."""
    global _config
    if _config is None:
        _config = Config.load()
    return _config


def save_config() -> None:
    """Save the global config."""
    if _config is not None:
        _config.save()
