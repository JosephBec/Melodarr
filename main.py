from mutagen.id3 import ID3, ID3NoHeaderError, TCON
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import subprocess
import shutil
import json
import os

# this is the main function
def download_songs(playlist_JSON_path: str, config_JSON_path: str):
    with open(playlist_JSON_path) as playlists: # first we get the info for the playlists
        playlist_content = playlists.read().strip()
        if not playlist_content:
            raise ValueError("❌ playlists.json is empty. Please add some playlists.")
        playlist_data = json.loads(playlist_content)

    with open(config_JSON_path) as config: # then we load in the data for the user config stuff
        config_content = config.read().strip()
        if not config_content:
            raise ValueError("❌ config.json is empty. Please add user data.")
        config_data = json.loads(config_content)

    for playlist in playlist_data: # loop through the different playlist urls
        url = playlist["url"] # this is from the playlist_json
        tags = playlist["tags"]

        youtube_dl_path = config_data["youtube_dl_path"] # all this is from config_json
        soundcloud_dl_path = config_data["soundcloud_dl_path"]
        spotify_dl_path = config_data["spotify_dl_path"]

        # put a check to make sure url and tags isn't empty

        platform = detect_platform(url)
        tags.insert(0, platform) #platform + genre

        if platform == "youtube":
            # download new playlist songs into temp folder
            yt_sc_mp3_downloader(url)
            
            # set tile = album for plex
            set_album_to_title("temp")
            
            # tag every file in the temp folder
            write_multiple_genres("temp", tags)
            
            # move every single file in the temp folder to the final location
            move_mp3s_to_destination("temp", youtube_dl_path)

            # download all json files for current playlist
            #yt_sc_json_downloader(url)
            dump_playlist_metadata_to_file(url, "temp/playlist.json")
            
            print()
            print()
            print()
            print()

            """
            # loop through all json files for current playlist
            for filename in os.listdir("temp"):
                song_title = None
                song_url = None
                if filename.endswith(".info.json"):
                    json_path = os.path.join("temp", filename)
                    try:
                        with open(json_path, "r", encoding="utf-8") as f:
                            metadata = json.load(f)
                            song_title = metadata.get("title", "Unknown Title")
                            song_url = metadata.get("webpage_url", "Unknown URL")
                    except Exception as e:
                        print(f"❌ Failed to read {filename}: {e}")

                print(song_url)
                verify_and_add_genres_if_missing(youtube_dl_path, song_title, tags, song_url)
            
                # make sure every json file corelates to a mp3 in destination folder
                
                # if that mp3 doesn't exist try and download it again
                
                # if mp3 does exist make sure that it has the correct tag
                
                # if mp3 does exist missing the tag correct it
            """
            #delete_all_json_files("temp")
            print()
            
        elif platform == "soundcloud":
            # download new playlist songs into temp folder
            #yt_sc_mp3_downloader(url)
            
            # set tile = album for plex
            #set_album_to_title("temp")
            
            # tag every file in the temp folder
            #write_multiple_genres("temp", tags)
            
            # move every single file in the temp folder to the final location
            #move_mp3s_to_destination("temp", soundcloud_dl_path)

            # download all json files for current playlist
            #yt_sc_json_downloader(url)
            
            # loop through all json files for current playlist
            
                # make sure every json file corelates to a mp3 in destination folder
                
                # if that mp3 doesn't exist try and download it again
                
                # if mp3 does exist make sure that it has the correct tag
                
                # if mp3 does exist missing the tag correct it

            print()
            
        elif platform == "spotify":
            # download new playlist songs into temp folder
            
            # set tile = album for plex
            
            # tag every file in the temp folder
            
            # move every single file in the temp folder to the final location
            print()
        
        else:
            print() # raise some error here too

def detect_platform(url): # real simple, used to properly tag the mp3's
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "soundcloud.com" in url:
        return "soundcloud"
    elif "spotify.com" in url:
        return "spotify"
    return "unknown"

def yt_sc_mp3_downloader(url): # so yt-dlp is used to download from both youtube (yt) and soundcloud (sc), spotify is gonna be something else
    youtube_command = [
        "yt-dlp",
        "-x", "--audio-format", "mp3", # final resulting files will be in mp3 format
        "--paths", "temp", # download them into the temp file
        "--embed-thumbnail", # self explanitory 
        "--add-metadata", # self explanitory 
        "--output", "%(title)s.%(ext)s", # file name is the gonna be title.extension (.mp3 for us)
        "--download-archive", "yt-dlp_archive.txt", # log the mp3 we downloaded, only download a mp3 if it hasn't been downloaded before 
        url
    ]

    subprocess.run(youtube_command, check=True)
    
def yt_sc_json_downloader(url): # this downloads an individual json for each song in a playlist
    youtube_json_command = [
        "yt-dlp",
        "--skip-download",
        "--paths", "temp",
        "--write-info-json",
        "--no-write-playlist-metafiles",
        url
    ]

    subprocess.run(youtube_json_command, check=True)

def spotify_downloader(url):
    zotify_command = [
        "zotify",
        "--download-format", "mp3",
        "--download-quality", "high",
        "--retry-attempts", "3",
        "--language", "en",
        "--root-path", "C:\Users\Joey\Desktop",
        "--output", "{song_name}.{ext}",
        url
    ]

def dump_playlist_metadata_to_file(playlist_url, output_path): # this downloads a single json for the whole playlist
    try:
        result = subprocess.run(
            ["yt-dlp", "--skip-download", "--dump-single-json", playlist_url],
            capture_output=True,
            text=True,
            check=True
        )

        # Create output folder if it exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Save output to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.stdout)

        print(f"✅ Playlist metadata saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ yt-dlp failed: {e.stderr}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def set_album_to_title(temp_dir): # plex groups by album, if a song doesn't have an album, it gets grouped into no album or something like that and forces every song to have the same cover art this circumvents that
    for filename in os.listdir(temp_dir):
        if filename.lower().endswith(".mp3"):
            mp3_path = os.path.join(temp_dir, filename)

            try:
                audio = EasyID3(mp3_path)

                title = audio.get("title", [None])[0]
                album = audio.get("album", [None])[0]

                print(title)
                print(album)
                print(filename.upper())

                if title:
                    audio["album"] = title
                    print(f"✅ Set album = title: {title}")
                elif title == album:
                    print(f"✔️ Album already matches title: {title}")
                else:
                    print(f"⚠️ No title in: {filename}, skipping album set")

                audio.save()

            except Exception as e:
                print(f"❌ Error processing {mp3_path}: {e}")

def verify_and_add_genres_if_missing(youtube_dl_path, song_title, genre_tags, song_url): # used to verify all the songs are downloaded and tagged propperly 
    filename = f"{song_title}.mp3" # this also is used for niche songs that are in multiple playlists. bc of the arhcive setting stopping us from downloading the same song
    filepath = os.path.join(youtube_dl_path, filename) # multiple times, we have to go and retag an existing song so it pops up in both playlists. 

    if not os.path.exists(filepath):
        print(f"❌ Missing: {filename} from playlist source: {song_url}")
        return False

    try:
        audio = MP3(filepath)

        if audio.tags is None:
            audio.add_tags()
            audio.save()
            audio = MP3(filepath)  # Re-load after saving tags

        existing_genres = []
        for frame in audio.tags.getall("TCON"):
            existing_genres.extend(frame.text)

        # Deduplicate and merge genres
        updated_genres = list(set(existing_genres + genre_tags))

        if set(genre_tags).issubset(set(existing_genres)):
            print(f"✅ All genre tags already present on: {filename}")
        else:
            # Update only if missing genres were found
            audio.tags.delall("TCON")
            audio.tags.add(TCON(encoding=3, text=updated_genres))
            audio.save(v2_version=4)
            print(f"🔄 Updated genres for {filename}: {updated_genres}")

        return True

    except Exception as e:
        print(f"❌ Error tagging {filename}: {e}")
        return False

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

def move_mp3s_to_destination(temp_dir, destination_dir): # we keep the songs in the temp directory, once we are done w the songs we move them with this function
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

def delete_all_json_files(folder): # clears out the temp folder from all the json files
    all_deleted = True

    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            file_path = os.path.join(folder, filename)
            try:
                os.remove(file_path)
            except Exception as e:
                all_deleted = False
                print(f"❌ Failed to delete {file_path}: {e}")

    if all_deleted:
        print("✅ Successfully cleared all .JSON files.")

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
