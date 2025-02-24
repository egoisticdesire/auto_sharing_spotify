import os
import subprocess

from dotenv import load_dotenv
from telethon.sync import TelegramClient
from config import settings



def get_spotify_track():
    apple_script = """
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
        result = (
            subprocess.check_output(["osascript", "-e", apple_script])
            .decode("utf-8")
            .strip()
        )

        if not result:
            return None, None

        track_id, track_title = result.split("|||")
        track_url = f'{settings.spotify.url}{track_id.split(":")[-1]}'
        return track_url, track_title

    except subprocess.CalledProcessError as e:
        return None, None


def send_track():
    track_url, track_title = get_spotify_track()
    if not track_url:
        print("ERROR")  # Report Shortcuts.app that the track is not played
        return

    with TelegramClient(
        settings.tg.session,
        settings.tg.api_id,
        settings.tg.api_hash,
    ) as client:
        message_suffix = f'🔥 <b><a href="{track_url}">{track_title}</a></b>'
        if "ru" in settings.system.language.lower():
            message = f"🎵 В <b>Spotify</b> сейчас играет:\n{message_suffix}"
        else:
            message = f"🎵 <b>Spotify</b> is playing now:\n{message_suffix}"

        client.send_message(
            entity=settings.tg.target_user_id,
            message=message,
            parse_mode=settings.tg.parse_mode,
            link_preview=settings.tg.link_preview,
        )
        print("OK")  # Report Shortcuts.app that everything is successful


if __name__ == "__main__":
    send_track()
