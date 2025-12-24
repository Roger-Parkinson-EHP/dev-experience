"""Main UI window for WhisperFlow - HAL 9000 inspired design."""

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QFrame,
    QHBoxLayout, QVBoxLayout, QGraphicsOpacityEffect,
    QGraphicsDropShadowEffect, QMenu
)
from PyQt6.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve,
    pyqtSignal, QSize, QPoint, QRect
)
from PyQt6.QtGui import QScreen, QFont, QPainter, QColor, QBrush, QPen, QRadialGradient
from enum import Enum
from typing import Optional, List
import random

from whisperflow.ui.styles import COLORS


class AppState(Enum):
    """Application states."""
    IDLE = "idle"
    RECORDING = "recording"
    PROCESSING = "processing"
    PREVIEW = "preview"
    LOADING = "loading"


class SoundWaveWidget(QWidget):
    """Sound wave visualization widget."""

    def __init__(self, num_bars: int = 12, parent=None):
        super().__init__(parent)
        self.num_bars = num_bars
        self.bar_heights = [0.2] * num_bars
        self.target_heights = [0.2] * num_bars
        self.setMinimumSize(120, 50)
        self.setMaximumHeight(50)

        # Animation timer
        self._timer = QTimer()
        self._timer.timeout.connect(self._animate)

    def start(self):
        """Start the animation."""
        self._timer.start(50)

    def stop(self):
        """Stop the animation."""
        self._timer.stop()
        self.bar_heights = [0.2] * self.num_bars
        self.update()

    def set_level(self, level: float):
        """Set the audio level (0-1)."""
        # Amplify level dramatically - typical speech is 0.01-0.1
        amplified = min(level * 50, 1.0)  # Amplify by 50x for dramatic visual

        # Create random target heights based on level
        for i in range(self.num_bars):
            base = 0.1 + amplified * 0.9  # Range 0.1-1.0
            variation = random.uniform(-0.3, 0.3) * amplified
            self.target_heights[i] = max(0.1, min(1.0, base + variation))

    def _animate(self):
        """Animate bars towards targets."""
        for i in range(self.num_bars):
            diff = self.target_heights[i] - self.bar_heights[i]
            self.bar_heights[i] += diff * 0.3
        self.update()

    def paintEvent(self, event):
        """Draw the sound wave bars."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        bar_width = w // (self.num_bars * 2)
        gap = bar_width
        total_width = self.num_bars * (bar_width + gap) - gap
        start_x = (w - total_width) // 2

        for i, height_ratio in enumerate(self.bar_heights):
            bar_height = int(h * height_ratio * 0.9)
            x = start_x + i * (bar_width + gap)
            y = (h - bar_height) // 2

            # Gradient from dark red to bright red
            gradient = QRadialGradient(x + bar_width/2, h/2, bar_width)
            gradient.setColorAt(0, QColor(COLORS['hal_red']))
            gradient.setColorAt(1, QColor(COLORS['hal_red_dark']))

            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(x, y, bar_width, bar_height, 2, 2)


class HALEyeWidget(QWidget):
    """HAL 9000 style eye widget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 50)
        self._glow_intensity = 0.5
        self._is_active = False

        # Glow animation
        self._glow_timer = QTimer()
        self._glow_timer.timeout.connect(self._pulse_glow)
        self._glow_direction = 1

    def set_active(self, active: bool):
        """Set whether the eye is active (recording)."""
        self._is_active = active
        if active:
            self._glow_timer.start(50)
        else:
            self._glow_timer.stop()
            self._glow_intensity = 0.3
        self.update()

    def set_intensity(self, level: float):
        """Set glow intensity based on audio level."""
        if self._is_active:
            # Amplify level for better visual (typical speech is 0.01-0.1)
            self._glow_intensity = 0.5 + min(level * 8, 0.5)
            self.update()

    def _pulse_glow(self):
        """Subtle pulse animation."""
        if not self._is_active:
            return
        self._glow_intensity += 0.02 * self._glow_direction
        if self._glow_intensity >= 1.0:
            self._glow_direction = -1
        elif self._glow_intensity <= 0.5:
            self._glow_direction = 1
        self.update()

    def paintEvent(self, event):
        """Draw the HAL 9000 eye."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        center_x = w // 2
        center_y = h // 2
        radius = min(w, h) // 2 - 2

        # Outer ring (dark)
        painter.setBrush(QColor(30, 30, 30))
        painter.setPen(QPen(QColor(60, 60, 60), 2))
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)

        # Inner glow gradient
        inner_radius = int(radius * 0.7)
        if self._is_active:
            # Active - red glow
            glow_color = QColor(255, int(50 * (1 - self._glow_intensity)), 0, int(255 * self._glow_intensity))
            gradient = QRadialGradient(center_x, center_y, inner_radius)
            gradient.setColorAt(0, QColor(255, 100, 50))
            gradient.setColorAt(0.5, QColor(255, 0, 0, int(200 * self._glow_intensity)))
            gradient.setColorAt(1, QColor(100, 0, 0, 50))
        else:
            # Idle - dim red
            gradient = QRadialGradient(center_x, center_y, inner_radius)
            gradient.setColorAt(0, QColor(150, 50, 50))
            gradient.setColorAt(0.5, QColor(100, 0, 0, 150))
            gradient.setColorAt(1, QColor(50, 0, 0, 50))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - inner_radius, center_y - inner_radius,
                           inner_radius * 2, inner_radius * 2)

        # Center bright spot
        spot_radius = int(radius * 0.2)
        if self._is_active:
            painter.setBrush(QColor(255, 200, 150, int(255 * self._glow_intensity)))
        else:
            painter.setBrush(QColor(200, 100, 100, 100))
        painter.drawEllipse(center_x - spot_radius, center_y - spot_radius,
                           spot_radius * 2, spot_radius * 2)


class WhisperFlowWindow(QWidget):
    """Main floating window for WhisperFlow - HAL 9000 style."""

    # Signals for thread-safe UI updates
    state_changed = pyqtSignal(AppState)
    text_ready = pyqtSignal(str)
    audio_level_changed = pyqtSignal(float)
    live_text_update = pyqtSignal(str)
    paste_last_requested = pyqtSignal()  # Signal for right-click "Paste Last"
    device_change_requested = pyqtSignal(object)  # Signal for device selection (int or None)
    toggle_mute_requested = pyqtSignal(bool)  # Signal for toggling mute setting
    toggle_auto_paste_requested = pyqtSignal(bool)  # Signal for toggling auto-paste

    # Size constants
    IDLE_WIDTH = 70
    IDLE_HEIGHT = 70
    EXPANDED_WIDTH = 450
    EXPANDED_HEIGHT = 100
    PREVIEW_HEIGHT = 120

    def __init__(self):
        super().__init__()
        self._current_state = AppState.LOADING
        self._preview_text = ""
        self._live_text = ""

        self._setup_window()
        self._setup_ui()
        self._connect_signals()

    def _setup_window(self) -> None:
        """Configure window properties."""
        self.setWindowTitle("LC Speech to Text")

        # Frameless, always on top, tool window (no taskbar icon)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        # Transparent background
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Set object name for styling
        self.setObjectName("MainWindow")

        # Initial size
        self.setFixedSize(self.IDLE_WIDTH, self.IDLE_HEIGHT)

        # Position at bottom center of screen
        self._position_window()

    def _position_window(self) -> None:
        """Position window at bottom center of primary screen."""
        screen = QApplication.primaryScreen()
        if screen:
            geometry = screen.availableGeometry()
            x = (geometry.width() - self.width()) // 2 + geometry.x()
            y = geometry.height() - self.height() - 80 + geometry.y()
            self.move(x, y)

    def _setup_ui(self) -> None:
        """Set up the UI elements."""
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Container frame (black background)
        self.container = QFrame()
        self.container.setObjectName("Container")
        self.container.setStyleSheet(f"""
            QFrame#Container {{
                background-color: {COLORS['background']};
                border-radius: 35px;
                border: 2px solid #333333;
            }}
        """)
        self.main_layout.addWidget(self.container)

        # Container layout
        self.container_layout = QHBoxLayout(self.container)
        self.container_layout.setContentsMargins(10, 10, 10, 10)
        self.container_layout.setSpacing(10)

        # HAL 9000 Eye
        self.hal_eye = HALEyeWidget()
        self.container_layout.addWidget(self.hal_eye, 0, Qt.AlignmentFlag.AlignCenter)

        # Sound wave widget (hidden initially)
        self.sound_wave = SoundWaveWidget()
        self.sound_wave.setVisible(False)
        self.container_layout.addWidget(self.sound_wave)

        # Status/text label (hidden initially)
        self.status_label = QLabel()
        self.status_label.setStyleSheet(f"""
            color: {COLORS['text']};
            font-size: 13px;
            font-family: 'Consolas', 'Monaco', monospace;
        """)
        self.status_label.setVisible(False)
        self.status_label.setWordWrap(True)
        self.status_label.setMaximumWidth(300)
        self.container_layout.addWidget(self.status_label, 1)

    def _connect_signals(self) -> None:
        """Connect signals to slots."""
        self.state_changed.connect(self._on_state_changed)
        self.text_ready.connect(self._on_text_ready)
        self.audio_level_changed.connect(self._on_audio_level)
        self.live_text_update.connect(self._on_live_text)

    def set_state(self, state: AppState) -> None:
        """Set the application state (thread-safe)."""
        self.state_changed.emit(state)

    def show_text(self, text: str) -> None:
        """Show transcribed text (thread-safe)."""
        self.text_ready.emit(text)

    def update_audio_level(self, level: float) -> None:
        """Update audio level visualization (thread-safe)."""
        self.audio_level_changed.emit(level)

    def update_live_text(self, text: str) -> None:
        """Update live transcription text (thread-safe)."""
        self.live_text_update.emit(text)

    def _on_state_changed(self, state: AppState) -> None:
        """Handle state change."""
        self._current_state = state

        if state == AppState.IDLE:
            self._show_idle()
        elif state == AppState.RECORDING:
            self._show_recording()
        elif state == AppState.PROCESSING:
            self._show_processing()
        elif state == AppState.PREVIEW:
            self._show_preview()
        elif state == AppState.LOADING:
            self._show_loading()

    def _on_text_ready(self, text: str) -> None:
        """Handle transcribed text."""
        self._preview_text = text
        if text:
            self.set_state(AppState.PREVIEW)

    def _on_audio_level(self, level: float) -> None:
        """Handle audio level update for visualization."""
        if self._current_state == AppState.RECORDING:
            self.hal_eye.set_intensity(level)
            self.sound_wave.set_level(level)

    def _on_live_text(self, text: str) -> None:
        """Handle live transcription text update."""
        self._live_text = text
        if self._current_state == AppState.RECORDING and text:
            self.status_label.setText(text[-100:])  # Show last 100 chars

    def _show_idle(self) -> None:
        """Show idle state - small HAL eye."""
        self.sound_wave.stop()
        self.sound_wave.setVisible(False)
        self.status_label.setText("")  # Clear text
        self.status_label.setVisible(False)
        self.hal_eye.set_active(False)
        self._preview_text = ""  # Clear preview text
        self._live_text = ""  # Clear live text

        self._animate_size(self.IDLE_WIDTH, self.IDLE_HEIGHT)

    def _show_recording(self) -> None:
        """Show recording state - HAL eye active with sound wave."""
        self.hal_eye.set_active(True)
        self.sound_wave.setVisible(True)
        self.sound_wave.start()
        self.status_label.setText("Listening...")
        self.status_label.setVisible(True)

        self._animate_size(self.EXPANDED_WIDTH, self.EXPANDED_HEIGHT)

    def _show_processing(self) -> None:
        """Show processing state."""
        self.sound_wave.stop()
        self.hal_eye.set_active(True)
        self.status_label.setText("Processing...")
        self.status_label.setVisible(True)

        self._animate_size(self.EXPANDED_WIDTH, self.EXPANDED_HEIGHT)

    def _show_preview(self) -> None:
        """Show preview state - show transcribed text briefly."""
        self.sound_wave.stop()
        self.sound_wave.setVisible(False)
        self.hal_eye.set_active(False)

        if self._preview_text:
            # Show first 150 chars
            display_text = self._preview_text[:150]
            if len(self._preview_text) > 150:
                display_text += "..."
            self.status_label.setText(display_text)
            self.status_label.setVisible(True)

        self._animate_size(self.EXPANDED_WIDTH, self.PREVIEW_HEIGHT)

        # Return to idle after delay
        QTimer.singleShot(2000, lambda: self.set_state(AppState.IDLE))

    def _show_loading(self) -> None:
        """Show loading state - waiting for model."""
        self.hal_eye.set_active(False)
        self.status_label.setText("Loading model...")
        self.status_label.setVisible(True)
        self.sound_wave.setVisible(False)

        self._animate_size(self.EXPANDED_WIDTH, self.EXPANDED_HEIGHT)

    def _animate_size(self, width: int, height: int) -> None:
        """Set window size."""
        self.setFixedSize(width, height)
        self._position_window()

    def mousePressEvent(self, event) -> None:
        """Handle mouse press for dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        """Handle mouse move for dragging."""
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, '_drag_pos'):
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def contextMenuEvent(self, event) -> None:
        """Show right-click context menu."""
        from whisperflow.audio import AudioRecorder

        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: #1a1a1a;
                color: white;
                border: 1px solid #333;
                padding: 5px;
            }}
            QMenu::item:selected {{
                background-color: #FF0000;
            }}
        """)

        # Copy last transcript
        paste_action = menu.addAction("📋 Copy Last Transcript")
        paste_action.triggered.connect(self.paste_last_requested.emit)

        menu.addSeparator()

        # Audio device submenu
        device_menu = menu.addMenu("🎤 Select Microphone")

        # Default device option
        default_action = device_menu.addAction("System Default")
        default_action.triggered.connect(lambda: self.device_change_requested.emit(None))

        device_menu.addSeparator()

        # List available input devices
        devices = AudioRecorder.get_input_devices()
        for device in devices:
            device_id = device['index']
            device_name = device['name'][:40]  # Truncate long names
            action = device_menu.addAction(device_name)
            action.triggered.connect(lambda checked, d=device_id: self.device_change_requested.emit(d))

        menu.addSeparator()

        # Settings submenu
        from whisperflow.utils.config import get_config
        config = get_config()

        settings_menu = menu.addMenu("⚙️ Settings")

        # Mute while recording toggle
        mute_action = settings_menu.addAction("🔇 Mute while recording")
        mute_action.setCheckable(True)
        mute_action.setChecked(config.pause_media_while_recording)
        mute_action.triggered.connect(lambda checked: self.toggle_mute_requested.emit(checked))

        # Auto-paste toggle
        paste_action = settings_menu.addAction("📋 Auto-paste after transcription")
        paste_action.setCheckable(True)
        paste_action.setChecked(config.auto_paste)
        paste_action.triggered.connect(lambda checked: self.toggle_auto_paste_requested.emit(checked))

        menu.exec(event.globalPos())

    @property
    def current_state(self) -> AppState:
        """Get the current application state."""
        return self._current_state
