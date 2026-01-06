# Christ In Song Hymnal

<div align="center">

**A modern, cross-platform desktop hymnal application**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)](https://wiki.qt.io/Qt_for_Python)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Downloads](https://img.shields.io/github/downloads/carrington-dev/christ-in-song/total.svg)]()

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Building](#building-from-source) • [Contributing](#contributing)

</div>

---

## 📖 About

**Christ In Song** is a feature-rich desktop hymnal application that brings the complete Christ In Song hymnal to your computer. Whether you're preparing for worship services, personal devotions, or leading congregational singing, this application provides an intuitive and modern interface for accessing hymns quickly and easily.

Built with modern technologies and designed for reliability, Christ In Song works seamlessly on Windows, macOS, and Linux.

## ✨ Features

### Core Features
- 🎵 **Complete Hymnal** - Access to all 695+ hymns from Christ In Song
- 🔍 **Powerful Search** - Search by number, title, lyrics, author, or composer
- ⭐ **Favorites System** - Mark and quickly access your favorite hymns
- 📜 **Recently Viewed** - Quick access to recently opened hymns
- 🎹 **Number Dialpad** - Fast hymn access via numeric keypad
- 📂 **Category Browser** - Browse hymns by topic (Worship, Praise, Prayer, etc.)

### User Experience
- 🎨 **Dark/Light Themes** - Comfortable viewing in any environment
- 🔤 **Adjustable Font Sizes** - Customize text size for readability
- ⌨️ **Keyboard Shortcuts** - Efficient navigation with hotkeys
- 📱 **Responsive Design** - Clean, modern interface that adapts to your screen
- 🖨️ **Print Support** - Print hymns for distribution
- 📋 **Copy to Clipboard** - Easy text copying for presentations

### Advanced Features
- 🎬 **Presentation Mode** - Full-screen display for projection
- 💾 **Automatic Backups** - Keep your favorites and settings safe
- 🔄 **Auto-Updates** - Stay current with the latest features
- 🌐 **Cross-Platform** - Works on Windows, macOS, and Linux
- 📊 **Usage Statistics** - Track your most-used hymns

## 🖥️ System Requirements

| Platform | Minimum Requirements |
|----------|---------------------|
| **Windows** | Windows 10 or later (64-bit) |
| **macOS** | macOS 10.15 (Catalina) or later |
| **Linux** | Ubuntu 20.04+ / Fedora 35+ / equivalent |
| **RAM** | 4 GB minimum, 8 GB recommended |
| **Storage** | 200 MB free disk space |

## 📥 Installation

### Windows

#### Option 1: Installer (Recommended)
1. Download the latest `ChristInSongSetup_v1.0.0.exe` from [Releases](https://github.com/carrington-dev/christ-in-song/releases)
2. Double-click the installer and follow the prompts
3. Launch from Start Menu or Desktop shortcut

#### Option 2: Portable Executable
1. Download `ChristInSong.exe` from [Releases](https://github.com/carrington-dev/christ-in-song/releases)
2. Run directly - no installation required!

### macOS
```bash
# Download the .dmg file from Releases
# Drag Christ In Song to Applications folder
# Launch from Applications
```

### Linux
```bash
# Ubuntu/Debian
wget https://github.com/carrington-dev/christ-in-song/releases/download/v1.0.0/christ-in-song_1.0.0_amd64.deb
sudo dpkg -i christ-in-song_1.0.0_amd64.deb

# Fedora/RHEL
wget https://github.com/carrington-dev/christ-in-song/releases/download/v1.0.0/christ-in-song-1.0.0.rpm
sudo rpm -i christ-in-song-1.0.0.rpm

# AppImage (Universal)
wget https://github.com/carrington-dev/christ-in-song/releases/download/v1.0.0/ChristInSong-1.0.0.AppImage
chmod +x ChristInSong-1.0.0.AppImage
./ChristInSong-1.0.0.AppImage
```

## 🚀 Quick Start

### First Launch
1. **Open the application** - Click the Christ In Song icon
2. **Browse hymns** - Use the list view or search functionality
3. **Find a hymn** - Enter a number on the dialpad or search by title
4. **Mark favorites** - Click the star icon on hymns you use frequently
5. **Customize** - Access Settings to adjust theme, font size, and preferences

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+F` | Open search |
| `Ctrl+H` | Go to home screen |
| `Ctrl+L` | Open hymn list |
| `Ctrl+D` | Toggle favorite |
| `Ctrl+P` | Print current hymn |
| `Ctrl+C` | Copy hymn text |
| `Ctrl++` | Increase font size |
| `Ctrl+-` | Decrease font size |
| `F11` | Toggle presentation mode |
| `←` `→` | Navigate previous/next hymn |

## 🛠️ Building from Source

### Prerequisites
- Python 3.9 or higher
- Git
- Virtual environment support

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/carrington-dev/christ-in-song.git
cd christ-in-song

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Run the application
python -m christ_in_song.main
```

### Build Executable

#### Windows
```bash
# Quick build
scripts\quick_build.bat

# Full build with installer (requires Inno Setup)
python scripts/build_windows.py
```

#### macOS
```bash
# Build .app bundle
python scripts/build_macos.py

# Create .dmg installer
python scripts/create_dmg.py
```

#### Linux
```bash
# Build AppImage
python scripts/build_appimage.py

# Build .deb package
python scripts/build_deb.py

# Build .rpm package
python scripts/build_rpm.py
```

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=christ_in_song --cov-report=html

# Run specific test file
pytest tests/test_database.py
```

## 📂 Project Structure

```
christ-in-song/
├── src/
│   └── christ_in_song/
│       ├── main.py              # Application entry point
│       ├── config.py            # Configuration management
│       ├── database/            # Database layer
│       ├── ui/                  # User interface components
│       ├── utils/               # Utility functions
│       └── resources/           # Icons, styles, data
├── installer/                   # Build configurations
├── tests/                       # Test suite
├── docs/                        # Documentation
├── scripts/                     # Build and utility scripts
├── pyproject.toml              # Project metadata
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## 🎨 Screenshots

<div align="center">

### Home Screen
![Home Screen](docs/screenshots/home.png)

### Hymn Display
![Hymn Display](docs/screenshots/hymn-view.png)

### Search Interface
![Search](docs/screenshots/search.png)

### Dark Theme
![Dark Theme](docs/screenshots/dark-theme.png)

</div>

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests
- 🌍 Translate the application
- ⭐ Star the repository

### Development Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Write or update tests
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📋 Roadmap

### Version 1.0 (Current)
- [x] Complete hymnal database
- [x] Search functionality
- [x] Favorites system
- [x] Dark/Light themes
- [x] Print support
- [x] Cross-platform builds

### Version 1.1 (Planned)
- [ ] Audio playback support
- [ ] Custom playlists
- [ ] Service planning features
- [ ] Cloud sync for favorites
- [ ] Mobile companion app

### Version 2.0 (Future)
- [ ] Multi-language support
- [ ] Chord charts
- [ ] Music notation display
- [ ] Community hymn sharing
- [ ] Integration with presentation software

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses
- **PySide6** - LGPL v3
- **Qt Framework** - LGPL v3
- **QtAwesome** - MIT License

## 🙏 Acknowledgments

- **Christ In Song Hymnal** - Original hymnal content
- **PySide6/Qt** - Excellent cross-platform framework
- **Contributors** - Thank you to all who have contributed to this project
- **Community** - Feedback and support from users

## 📞 Support

### Get Help
- 📖 Read the [User Guide](docs/user_guide.md)
- 💬 Join our [Discussions](https://github.com/carrington-dev/christ-in-song/discussions)
- 🐛 Report bugs via [Issues](https://github.com/carrington-dev/christ-in-song/issues)
- 📧 Email: carrington.muleya@outlook.com

### Community
- ⭐ Star this repo to show support
- 🔄 Share with your church community
- 📢 Spread the word on social media

## 📊 Statistics

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/carrington-dev/christ-in-song?style=social)
![GitHub forks](https://img.shields.io/github/forks/carrington-dev/christ-in-song?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/carrington-dev/christ-in-song?style=social)

</div>

---

<div align="center">

**Made with ❤️ for the worship community**

[Website](https://carrington-dev.github.io/christ-in-song) • [GitHub](https://github.com/carrington-dev/christ-in-song) • [Report Bug](https://github.com/carrington-dev/christ-in-song/issues) • [Request Feature](https://github.com/carrington-dev/christ-in-song/issues)

</div>