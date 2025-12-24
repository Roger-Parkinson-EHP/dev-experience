"""QSS styles for WhisperFlow UI."""

# Colors - HAL 9000 inspired theme
COLORS = {
    "primary": "#3B82F6",      # Blue
    "primary_dark": "#2563EB",
    "secondary": "#10B981",    # Green
    "background": "#000000",   # Black (HAL style)
    "background_light": "#1a1a1a",
    "text": "#FFFFFF",
    "text_muted": "#888888",
    "recording": "#FF0000",    # HAL red
    "recording_glow": "#FF3333",
    "processing": "#FF6600",   # Orange
    "hal_red": "#FF0000",
    "hal_red_dark": "#990000",
    "hal_red_glow": "#FF3333",
}

# Main window styles
MAIN_WINDOW_STYLE = """
QWidget#MainWindow {
    background-color: transparent;
}
"""

# Container styles (the visible part)
CONTAINER_STYLE = f"""
QFrame#Container {{
    background-color: {COLORS['background']};
    border-radius: 25px;
    border: 2px solid {COLORS['background_light']};
}}
"""

# Idle indicator (small circle)
IDLE_INDICATOR_STYLE = f"""
QLabel#IdleIndicator {{
    background-color: {COLORS['primary']};
    border-radius: 20px;
    min-width: 40px;
    max-width: 40px;
    min-height: 40px;
    max-height: 40px;
}}
"""

# Recording indicator
RECORDING_INDICATOR_STYLE = f"""
QLabel#RecordingIndicator {{
    background-color: {COLORS['recording']};
    border-radius: 20px;
    min-width: 40px;
    max-width: 40px;
    min-height: 40px;
    max-height: 40px;
}}
"""

# Processing indicator
PROCESSING_INDICATOR_STYLE = f"""
QLabel#ProcessingIndicator {{
    background-color: {COLORS['processing']};
    border-radius: 20px;
    min-width: 40px;
    max-width: 40px;
    min-height: 40px;
    max-height: 40px;
}}
"""

# Status label
STATUS_LABEL_STYLE = f"""
QLabel#StatusLabel {{
    color: {COLORS['text']};
    font-size: 14px;
    font-weight: bold;
    padding: 0 10px;
}}
"""

# Text preview label
TEXT_PREVIEW_STYLE = f"""
QLabel#TextPreview {{
    color: {COLORS['text']};
    font-size: 13px;
    padding: 5px 15px;
    background-color: transparent;
}}
"""

# Combined stylesheet
STYLESHEET = f"""
{MAIN_WINDOW_STYLE}
{CONTAINER_STYLE}
{IDLE_INDICATOR_STYLE}
{STATUS_LABEL_STYLE}
{TEXT_PREVIEW_STYLE}
"""
