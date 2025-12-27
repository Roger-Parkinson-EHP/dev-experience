# Speech-to-Text

Voice dictation tools for developers.

## Recommended: WisprFlow

For best accuracy and fluency, use **[WisprFlow](https://wisprflow.com)** ($8/month):

- LLM post-processing cleans up raw transcription
- Much better fluency than raw Whisper
- Works in any app (Ctrl+Win+Space)
- 14-day free trial

**Setup:**
1. Download from [wisprflow.com](https://wisprflow.com)
2. Install and sign in
3. Decline training data usage if desired
4. Use Ctrl+Win+Space to dictate

---

## Alternative: LocalWhisper

If you need **100% local/offline** transcription, use LocalWhisper below. It's free but produces raw Whisper output without LLM cleanup.

### Privacy

- **100% Local**: All transcription happens on your machine using faster-whisper
- **No Cloud**: Audio never leaves your computer
- **No Training**: Your voice data is never used to train models
- **No Account Required**: Works completely offline after initial setup

## Features

- **Hotkey activation**: Ctrl+Shift+Space to start/stop recording
- **Streaming transcription**: Processes audio in real-time during recording
- **Auto-mute**: System audio mutes during recording
- **Auto-paste**: Transcribed text pastes automatically
- **Custom vocabulary**: Add domain-specific terms for better recognition
- **HAL 9000 UI**: Visual indicator when recording

## Setup

### Windows

```powershell
cd speech-to-text/local_whisper

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

1. Start LocalWhisper (`python main.py`)
2. Look for the HAL 9000 eye indicator
3. Press **Ctrl+Shift+Space** to start recording
4. Speak your text
5. Press **Ctrl+Shift+Space** again to stop
6. Text is transcribed and pasted

## Configuration

Settings are stored in `~/.whisperflow/config.json`:

```json
{
  "model_size": "base",
  "hotkey": "ctrl+shift+space",
  "auto_paste": true,
  "language": "en",
  "show_preview": true,
  "audio_device_id": null,
  "pause_media_while_recording": true,
  "custom_vocabulary": "Claude, Bazel, LocalWhisper, GitHub"
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `model_size` | `base` | Whisper model (tiny/base/small/medium/large) |
| `language` | `en` | Target language |
| `hotkey` | `ctrl+shift+space` | Activation hotkey |
| `auto_paste` | `true` | Automatically paste after transcription |
| `pause_media_while_recording` | `true` | Mute system audio during recording |
| `custom_vocabulary` | `""` | Comma-separated terms for better recognition |
| `audio_device_id` | `null` | Specific microphone (null = system default) |

Larger models are more accurate but slower. `base` is a good balance.

## Custom Vocabulary

Add domain-specific terms to improve recognition accuracy:

```json
"custom_vocabulary": "Claude Code, Anthropic, Bazel, FedRAMP, licensecorporation-dev, Vertex AI"
```

These terms are passed to Whisper as an `initial_prompt`, biasing recognition toward your vocabulary.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No transcription | Check microphone permissions |
| Double paste | Restart LocalWhisper |
| Mute not working | Run as Administrator (Windows) |
| Slow transcription | Use smaller model or enable CUDA |

## Architecture

LocalWhisper uses **streaming transcription**:

1. Audio is captured in real-time via `sounddevice`
2. Every 3 seconds, a chunk is sent to faster-whisper
3. Partial results display as you speak
4. On release, final text is ready almost instantly

This is faster than batch mode (transcribing all audio after recording stops).

## Alternatives

| Tool | Pros | Cons |
|------|------|------|
| **LocalWhisper** (this) | 100% local, no account, free | Raw Whisper output, no LLM cleanup |
| **WisprFlow** | LLM post-processing, better fluency | Cloud-based, subscription required |
| **Aqua Voice** | Best accuracy, screen context | Cloud-based, subscription required |

## Future Improvements

- [ ] LLM post-processing for improved fluency (via Gemini MCP)
- [ ] Screen context awareness
- [ ] Voice commands ("scratch that", "new paragraph")
- [ ] Model selection per-recording (speed vs accuracy)
