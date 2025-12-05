# EJ Tools 🚀

A powerful, stylish, and user-friendly Command Line Interface (CLI) to download videos and audio from various platforms (YouTube, Instagram, TikTok, Twitter/X, and more). Built with Python, powered by yt-dlp, and styled with Rich.

![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)
![Powered by yt-dlp](https://img.shields.io/badge/Powered%20by-yt--dlp-red)
![Dependency FFmpeg](https://img.shields.io/badge/Dependency-FFmpeg-green)

## ✨ Features

- **High Quality Video**: Download videos up to 4K resolution.
- **Audio Extraction**: Convert videos to MP3 (High/Medium/Low quality) with metadata.
- **Video Only Mode**: Option to download video streams without audio (muted).
- **Smart Selection**: Automatically selects the best bitrate and codecs (VP9/AV1/H.264).
- **Custom Settings**: Set a persistent custom download folder via the Settings menu.
- **Beautiful UI**: Interactive menus, progress bars, and ASCII art banners using Rich and Questionary.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

## 🛠️ Prerequisites

Before running the tool, ensure you have the following:

1. Python 3.8+ installed.
2. FFmpeg installed (Crucial for 4K merging and MP3 conversion).

### Setting up FFmpeg

- **Windows**: Download `ffmpeg.exe` and `ffprobe.exe` and place them in the same folder as the script (or add them to your System PATH).
- **Mac/Linux**: Install via terminal: `brew install ffmpeg` or `sudo apt install ffmpeg`.

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tu-usuario/EJ-Tools.git
   cd EJ-Tools
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```



## 🚀 Usage

Run the script directly with Python:
```bash
python main.py
```

Follow the interactive menu:

1. Choose between Video, Video (No Audio), or Audio.
2. Paste the link (Ctrl+V).
3. Select quality.
4. Done! 🍿

## ⚙️ Configuration

You can change the default download location inside the tool:

- Select **Settings** in the main menu.
- Choose **Change Download Path**.
- Enter your desired absolute path (e.g., `C:/Users/Name/Downloads`).
- The path is saved in `settings.json` automatically.

## 📦 Building an Executable (.exe)

Want to share this with friends who don't have Python? Build a standalone .exe:

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build the file:
   ```bash
   pyinstaller --onefile --name "EJTools" main.py
   ```

3. **Important**: Copy `ffmpeg.exe` and `ffprobe.exe` into the same folder as your new `EJTools.exe` for it to work correctly on other computers.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 👤 Author

[@ej3mplo](https://github.com/ej3mplo)

- **Twitter/X**: [@ej3mplo](https://twitter.com/ej3mplo)
- **Github**: [@ej3mplo](https://github.com/ej3mplo)

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
