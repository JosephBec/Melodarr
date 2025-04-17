from mutagen.easyid3 import EasyID3
import subprocess
import json
import os

def download_songs(playlist_JSON_path: str, config_JSON_path: str):
    with open(playlist_JSON_path) as playlists:
        playlist_content = playlists.read().strip()
        if not playlist_content:
            raise ValueError("❌ playlists.json is empty. Please add some playlists.")
        playlist_data = json.loads(playlist_content)

    with open(config_JSON_path) as config:
        config_content = config.read().strip()
        if not config_content:
            raise ValueError("❌ config.json is empty. Please add user data.")
        config_data = json.loads(config_content)

    for playlist in playlist_data:
        url = playlist["url"]
        tags = playlist["tags"]

        # put a check to make sure url and tags isn't empty

        platform = detect_platform(url)
        tags.insert(0, platform) #platform + genre

        if platform == "youtube":
            # download new playlist songs into temp folder
            youtube_download(url)
            
            # set tile = album for plex
            set_album_to_title("temp")
            
            # tag every file in the temp folder
            
            # move every single file in the temp folder to the final location
            print()
            
        elif platform == "soundcloud":
            # download new playlist songs into temp folder
            
            # set tile = album for plex
            
            # tag every file in the temp folder
            
            # move every single file in the temp folder to the final location
            print()
            
        elif platform == "spotify":
            # download new playlist songs into temp folder
            
            # set tile = album for plex
            
            # tag every file in the temp folder
            
            # move every single file in the temp folder to the final location
            print()
        
        else:
            print() # raise some error here too

def detect_platform(url):
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "soundcloud.com" in url:
        return "soundcloud"
    elif "spotify.com" in url:
        return "spotify"
    return "unknown"

def youtube_download(url):
    youtube_command = [
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "--paths", "temp",
        "--embed-thumbnail",
        "--add-metadata",
        "--output", "%(title)s.%(ext)s",
        "--download-archive", "yt-dlp_archive.txt",
        url
    ]

    subprocess.run(youtube_command, check=True)

def set_album_to_title(temp_dir):
    for filename in os.listdir(temp_dir):
        if filename.lower().endswith(".mp3"):
            mp3_path = os.path.join(temp_dir, filename)

            try:
                audio = EasyID3(mp3_path)

                title = audio.get("title", [None])[0]
                album = audio.get("album", [None])[0]

                if title and album is None:
                    audio["album"] = title
                    print(f"✅ Set album = title: {title}")
                elif title == album:
                    print(f"✔️ Album already matches title: {title}")
                else:
                    print(f"⚠️ No title in: {filename}, skipping album set")

                audio.save()

            except Exception as e:
                print(f"❌ Error processing {mp3_path}: {e}")

def main():
    

    download_songs("playlists.json", "config.json")

    """
    #os.makedirs("downloads", exist_ok=True)
    """

if __name__ == "__main__":
    main()

"""

#soundcloud_url = r"https://soundcloud.com/interscope/rixton-me-and-my-broken-heart"
soundcloud_command = ["scdl", "-l", soundcloud_url]
subprocess.run(soundcloud_command, check=True)


youtube_url = "https://www.youtube.com/playlist?list=PLKIsbG8iT8bsNTizG8Byx2goiWU3nBxs6"
youtube_command = [
    "yt-dlp",
    "-x", "--audio-format", "mp3",
    "--paths", "temp",
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