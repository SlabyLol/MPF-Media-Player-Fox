# MPF - MediaPlayerFox Pro 🦊

**MPF (MediaPlayerFox)** is a high-performance, modern media player built with Python and PyQt6. It features a dynamic circular beat visualizer for audio files and seamless high-definition video playback. Designed by **DarkFox Co.** for coders and power users.

## ✨ Features

* **Dual Mode Engine:** Automatically switches between a pulsing Audio Visualizer and a sleek Video Player.
* **Dynamic Visualizer:** Real-time "beat" animation that pulses with the audio, featuring the custom MPF icon at its core.
* **Broad Format Support:** Plays `.mp3`, `.wav`, `.ogg`, `.mp4`, `.mkv`, `.avi`, and `.m4a`.
* **Cinema Experience:** Full-screen support with `F11` and quick exit with `Esc`.
* **Modern UI:** A minimalist dark-themed interface with "Fox Orange" accents.
* **Volume Control:** Precision slider for real-time audio output management.

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.9+ installed. You will need the following libraries:

```bash
pip install PyQt6 pyqtgraph numpy pyinstaller 
```
To make the programm go to your file directory paste it and go to cmd
```bash
cd directory/directory
```
Then put this command in:
```bash
pyinstaller --noconfirm --onefile --windowed --icon="mpf-icon-ico.ico" --add-data "mpf-icon-ico.ico;." MPF.py
```
