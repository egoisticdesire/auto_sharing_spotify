import os
import subprocess

from dotenv import load_dotenv
from telethon.sync import TelegramClient

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
TARGET_USER_ID = os.getenv("TARGET_USER_ID")

if not API_ID or not API_HASH or not TARGET_USER_ID:
    # raise ValueError("❌ All environment variables are not set!")
    raise ValueError("❌ Не заданы все переменные окружения!")

API_ID = int(API_ID)
TARGET_USER_ID = int(TARGET_USER_ID)


def get_spotify_track():
    script = """
    tell application "Spotify"
        if player state is playing then
            set trackID to id of current track
            set trackName to name of current track
            set artistName to artist of current track
            if trackID starts with "spotify:track:" then
                return trackID & "|||" & artistName & " － " & trackName
            end if
        end if
    end tell
    """
    try:
        result = subprocess.check_output(["osascript", "-e", script]).decode("utf-8").strip()
        if not result:
            return None, None
        track_id, track_title = result.split("|||")
        track_url = f"https://open.spotify.com/track/{track_id.split(":")[-1]}"
        return track_url, track_title
    except subprocess.CalledProcessError:
        return None, None


def send_track():
    track_url, track_title = get_spotify_track()
    if not track_url:
        print("ERROR")  # Report Shortcuts.app that the track is not played
        return

    with TelegramClient("session", API_ID, API_HASH) as client:
        # message = f'🎵 <b>Spotify</b> is playing now:\n🔥 <b><a href="{track_url}">{track_title}</a></b>'
        message = f'🎵 В <b>Spotify</b> сейчас играет:\n🔥 <b><a href="{track_url}">{track_title}</a></b>'
        client.send_message(
            TARGET_USER_ID,
            message,
            parse_mode="html",
            link_preview=False,
        )
        print("OK")  # Report Shortcuts.app that everything is successful


if __name__ == "__main__":
    send_track()
