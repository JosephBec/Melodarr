from mutagen.id3 import ID3, ID3NoHeaderError, TCON
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import subprocess
import shutil
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

        youtube_dl_path = config_data["youtube_dl_path"]
        soundcloud_dl_path = config_data["soundcloud_dl_path"]
        spotify_dl_path = config_data["spotify_dl_path"]

        # put a check to make sure url and tags isn't empty

        platform = detect_platform(url)
        tags.insert(0, platform) #platform + genre

        if platform == "youtube":
            # download new playlist songs into temp folder
            youtube_download(url)
            
            # set tile = album for plex
            set_album_to_title("temp")
            
            # tag every file in the temp folder
            write_multiple_genres("temp", tags)
            
            # move every single file in the temp folder to the final location
            move_mp3s_to_destination("temp", youtube_dl_path)
            
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

def write_multiple_genres(temp_dir, genre_list):
    """
    Sets multiple genre tags on each .mp3 file in temp_dir using ID3v2.4.
    Overwrites any existing genre data.
    """
    for filename in os.listdir(temp_dir):
        if filename.lower().endswith(".mp3"):
            mp3_path = os.path.join(temp_dir, filename)

            try:
                # Load MP3 and access ID3 tags
                audio = MP3(mp3_path)

                # Add tag block if missing
                if audio.tags is None:
                    audio.add_tags()
                    audio.save()

                # Clear previous genres
                audio.tags.delall("TCON")

                # Add new genres
                audio.tags.add(TCON(encoding=3, text=genre_list))

                # Save with ID3v2.4
                audio.save(v2_version=4)

                print(f"✅ Set genres on {filename}: {genre_list}")

            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

def set_genre_tags(temp_dir, genre_tags):
    for filename in os.listdir(temp_dir):
        if filename.lower().endswith(".mp3"):
            mp3_path = os.path.join(temp_dir, filename)

            try:
                audio = EasyID3(mp3_path)
                audio["genre"] = "\\".join(genre_tags)
                audio.save()
                print(f"🏷️ Set genre on {filename}: {', '.join(genre_tags)}")

            except Exception as e:
                print(f"❌ Error setting genre for {mp3_path}: {e}")

def move_mp3s_to_destination(temp_dir, destination_dir):
    os.makedirs(destination_dir, exist_ok=True)

    for filename in os.listdir(temp_dir):
        if filename.lower().endswith(".mp3"):
            src = os.path.join(temp_dir, filename)
            dest = os.path.join(destination_dir, filename)

            try:
                shutil.move(src, dest)
                print(f"📦 Moved {filename} to {destination_dir}")
            except Exception as e:
                print(f"❌ Failed to move {filename}: {e}")

def main():
    

    download_songs("playlists.json", "config.json")

    """
    #os.makedirs("downloads", exist_ok=True)
    """

if __name__ == "__main__":
    main()

#soundcloud_url = r"https://soundcloud.com/interscope/rixton-me-and-my-broken-heart"
#soundcloud_command = ["scdl", "-l", soundcloud_url]
#subprocess.run(soundcloud_command, check=True)
