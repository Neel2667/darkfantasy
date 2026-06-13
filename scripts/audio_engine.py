import subprocess
import os

class AudioEngine:
    def __init__(self, music_dir="psycho_studio/assets/music", sfx_dir="psycho_studio/assets/sfx"):
        self.music_dir = music_dir
        self.sfx_dir = sfx_dir

    def get_ducking_filter(self, voice_delay=0.5):
        """
        Returns an FFmpeg filter string that ducks music when voice is present.
        In a simplified version, we'll use a fixed sidechain-like volume drop.
        """
        # [1:a] is voice, [2:a] is music
        # This filter lowers volume of [2:a] when [1:a] has signal
        return "sidechaincompress=threshold=0.03:ratio=20:attack=200:release=1000"

    def get_sfx_path(self, cue_name):
        # Maps "whoosh" to "assets/sfx/whoosh_01.mp3"
        sfx_map = {
            "whoosh": "whoosh_cinematic.mp3",
            "glitch": "glitch_static.mp3",
            "thud": "deep_impact.mp3",
            "heartbeat": "heartbeat_loop.mp3"
        }
        filename = sfx_map.get(cue_name.lower(), "whoosh_cinematic.mp3")
        return os.path.join(self.sfx_dir, filename)

    def get_music_path(self, mood):
        # Maps "dark_ambient" to "assets/music/dark_ambient_01.mp3"
        music_map = {
            "dark_ambient": "dark_tension.mp3",
            "tense_rhythm": "aggressive_dark.mp3",
            "ominous_drone": "deep_drone.mp3"
        }
        filename = music_map.get(mood.lower(), "dark_tension.mp3")
        return os.path.join(self.music_dir, filename)
