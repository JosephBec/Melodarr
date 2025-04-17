from mutagen.easyid3 import EasyID3
import subprocess
import json
import os

def detect_platform(url):
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "soundcloud.com" in url:
        return "soundcloud"
    elif "spotify.com" in url:
        return "spotify"
    return "unknown"

def set_album_same_as_title(mp3_path):
    try:
        audio = EasyID3(mp3_path)
        title = audio.get("title", [None])[0]
        album = audio.get("album", [None])[0]
        if title and album is None:
            audio["album"] = title
            audio.save()
            print(f"✅ Set album tag to match title: {title}")
        elif title == album:
            print(f"{title} ✅ Album tag and title match")
        else:
            print(f"⚠️ No title found in {mp3_path}, skipping album tag update.")
    except Exception as e:
        print(f"❌ Error editing {mp3_path}: {e}")


def main():
    with open("playlists.json") as f:
        playlist_data = json.load(f)

    os.makedirs("downloads", exist_ok=True)

if __name__ == "__main__":
    main()

"""
soundcloud_url = "https://soundcloud.com/interscope/rixton-me-and-my-broken-heart"
soundcloud_command = ["scdl", "-l", soundcloud_url]
subprocess.run(soundcloud_command, check=True)


youtube_url = "https://www.youtube.com/playlist?list=PLKIsbG8iT8bsNTizG8Byx2goiWU3nBxs6"
youtube_command = [
    "yt-dlp",
    "-x", "--audio-format", "mp3",
    "--paths", r"E:\Plex\Music\Youtube",
    "--embed-thumbnail",
    "--add-metadata",
    "--output", "%(title)s.%(ext)s",
    "--download-archive", "yt-dlp_archive.txt",
    youtube_url
]

subprocess.run(youtube_command, check=True)

#set_album_same_as_title(r"D:\Projects\Melodarr\Coldplay - Viva La Vida (Official Video).mp3")
#set_album_same_as_title(r"D:\Projects\Melodarr\O-Zone - Dragostea Din Tei [Official Video].mp3")
#set_album_same_as_title(r"D:\Projects\Melodarr\Rick Astley - Never Gonna Give You Up (Official Music Video).mp3")

"""