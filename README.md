# 🎶 Melodarr

**Melodarr** is an automated music downloader and organizer that integrates with Plexamp. It fetches tracks from various platforms, tags them appropriately, and organizes them into a Plex-friendly structure.

## 🚀 Features

- **Multi-Source Downloading**: Supports YouTube, SoundCloud, and Spotify.
- **Automated Tagging**: Utilizes open-source taggers to ensure accurate metadata.
- **Playlist Tracking**: Monitors playlists for updates and downloads new tracks automatically.
- **Plex Integration**: Organizes music into a structure compatible with Plexamp.

## 🛠️ Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/melodarr.git
   cd melodarr
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📁 Directory Structure

```
melodarr/
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
├── LICENSES/
│   ├── yt-dlp.txt
│   ├── scdl.txt
│   └── spotdl.txt
├── temp/
```

## 📄 License

Melodarr is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

## 🤝 Acknowledgments

Melodarr leverages the following open-source projects:

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [zotify](https://github.com/zotify-dev/zotify)
- [mutagen](https://mutagen.readthedocs.io/en/latest/)

Please refer to the `LICENSES/` directory for detailed license information of these dependencies.
