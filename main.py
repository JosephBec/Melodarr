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
            raise ValueError("❌ config.json is empty. Please add some playlists.")
        config_data = json.loads(config_content)

    for playlist in playlist_data:
        url = playlist["url"]
        tags = playlist["tags"]
        print(url)

        platform = detect_platform(url)
        print(platform)

        tags.insert(0, platform)
        print(tags)
        print()
    
    #loop for every entry in JSON tracking file
        #platform = detect_platform()
        #platform + genre


        #platform = youtube
        #download new playlist songs into youtube folder found in user_config
        #set title = album for plex
        #check every mp3 in youtube folder is tagged

        
        #platform = soundcloud
        #download new playlist songs into soundcloud folder found in user_config
        #set title = album for plex
        #check every mp3 in soundcloud folder is tagged

        
        #platform = spotify
        #download new playlist songs into spotify folder found in user_config
        #set title = album for plex
        #check every mp3 in spotify folder is tagged
    


def detect_platform(url):
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "soundcloud.com" in url:
        return "soundcloud"
    elif "spotify.com" in url:
        return "spotify"
    return "unknown"

def tag_mp3(mp3_path):
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