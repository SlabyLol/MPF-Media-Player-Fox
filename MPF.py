import sys
import os
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QFileDialog, QLabel, QHBoxLayout, QStackedWidget, 
                             QSlider, QFrame)
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtGui import QKeyEvent, QPainter, QPen, QColor, QIcon, QPixmap

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class VisualizerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.points = 80
        self.amplitude = 0
        self.base_radius = 100
        self.color = QColor("#ff7b00")
        self.icon_path = resource_path("mpf-icon-ico.ico")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)

    def set_amplitude(self, value):
        self.amplitude = value

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        center = self.rect().center()
        
        painter.setPen(QPen(self.color, 4))
        for i in range(self.points):
            angle = (i / self.points) * 2 * np.pi
            dynamic_radius = self.base_radius + (np.random.randint(0, self.amplitude + 10) if self.amplitude > 0 else 0)
            x1 = center.x() + int(np.cos(angle) * self.base_radius)
            y1 = center.y() + int(np.sin(angle) * self.base_radius)
            x2 = center.x() + int(np.cos(angle) * dynamic_radius)
            y2 = center.y() + int(np.sin(angle) * dynamic_radius)
            painter.drawLine(x1, y1, x2, y2)
        
        icon_pixmap = QPixmap(self.icon_path)
        if not icon_pixmap.isNull():
            size = 120 + (self.amplitude // 4)
            scaled_icon = icon_pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            painter.drawPixmap(center.x() - size // 2, center.y() - size // 2, scaled_icon)

class MediaPlayerFox(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MPF - Media Player Fox")
        self.resize(1100, 800)
        
        icon_path = resource_path("mpf-icon-ico.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setStyleSheet("background-color: #050505; color: #ffffff; font-family: 'Segoe UI';")

        self.mediaPlayer = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.audioOutput.setVolume(0.7)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.display_stack = QStackedWidget()
        self.visualizer = VisualizerWidget()
        self.videoWidget = QVideoWidget()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        
        self.display_stack.addWidget(self.visualizer)
        self.display_stack.addWidget(self.videoWidget)
        self.main_layout.addWidget(self.display_stack)

        self.setup_ui()

    def setup_ui(self):
        self.ctrl_frame = QFrame()
        self.ctrl_frame.setFixedHeight(110)
        self.ctrl_frame.setStyleSheet("background: #111; border-top: 2px solid #ff7b00;")
        layout = QHBoxLayout(self.ctrl_frame)

        btn_open = QPushButton("OPEN FILE")
        btn_open.setFixedSize(120, 45)
        btn_open.clicked.connect(self.open_media)
        btn_open.setStyleSheet("background: #222; border: 1px solid #ff7b00; font-weight: bold;")

        btn_play = QPushButton("PLAY / PAUSE")
        btn_play.setFixedSize(120, 45)
        btn_play.clicked.connect(self.toggle_playback)
        btn_play.setStyleSheet("background: #ff7b00; color: black; font-weight: bold;")

        self.vol_slider = QSlider(Qt.Orientation.Horizontal)
        self.vol_slider.setRange(0, 100)
        self.vol_slider.setValue(70)
        self.vol_slider.setFixedWidth(150)
        self.vol_slider.valueChanged.connect(lambda v: self.audioOutput.setVolume(v/100))

        copy_info = QLabel("© 2026 DarkFox Co.")
        copy_info.setStyleSheet("color: #444; font-size: 10px;")

        layout.addWidget(btn_open)
        layout.addWidget(btn_play)
        layout.addStretch()
        layout.addWidget(QLabel("VOLUME"))
        layout.addWidget(self.vol_slider)
        layout.addWidget(copy_info)
        self.main_layout.addWidget(self.ctrl_frame)

    def open_media(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "MPF - Select Media", "", "Supported Files (*.mp3 *.wav *.ogg *.mp4 *.mkv *.avi)")
        if file_path:
            self.mediaPlayer.setSource(QUrl.fromLocalFile(file_path))
            is_vid = file_path.lower().endswith(('.mp4', '.mkv', '.avi'))
            self.display_stack.setCurrentIndex(1 if is_vid else 0)
            self.mediaPlayer.play()
            self.visualizer.set_amplitude(45)

    def toggle_playback(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.mediaPlayer.pause()
            self.visualizer.set_amplitude(0)
        else:
            self.mediaPlayer.play()
            self.visualizer.set_amplitude(45)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F11:
            if self.isFullScreen(): self.showNormal()
            else: self.showFullScreen()
        elif event.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self.showNormal()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MediaPlayerFox()
    window.show()
    sys.exit(app.exec())
