# Speech-to-Text (WhisperFlow)

Local speech-to-text using OpenAI Whisper. Press a hotkey, speak, and text is pasted into your active window.

## Features

- **Hotkey activation**: Ctrl+Shift+Space to start/stop recording
- **Auto-mute**: System audio mutes during recording
- **Auto-paste**: Transcribed text pastes automatically
- **Local processing**: All transcription happens on your machine
- **HAL 9000 UI**: Visual indicator when recording

## Setup

### Windows

```powershell
cd speech-to-text/whisperflow

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### Requirements

- Python 3.10+
- CUDA-capable GPU (optional, for faster transcription)
- ~1GB disk space for Whisper models

## Usage

1. Start WhisperFlow (`python main.py`)
2. Look for the HAL 9000 eye indicator
3. Press **Ctrl+Shift+Space** to start recording
4. Speak your text
5. Press **Ctrl+Shift+Space** again to stop
6. Text is transcribed and pasted

## Configuration

Edit `utils/config.py` to customize:

| Setting | Default | Description |
|---------|---------|-------------|
| `MODEL_SIZE` | `base` | Whisper model (tiny/base/small/medium/large) |
| `LANGUAGE` | `en` | Target language |
| `HOTKEY` | `ctrl+shift+space` | Activation hotkey |

Larger models are more accurate but slower. `base` is a good balance.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No transcription | Check microphone permissions |
| Double paste | Restart WhisperFlow |
| Mute not working | Run as Administrator (Windows) |
| Slow transcription | Use smaller model or enable CUDA |
