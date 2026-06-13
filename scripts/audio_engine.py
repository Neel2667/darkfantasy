import subprocess
import os

class AudioEngine:
    def __init__(self, music_dir="assets/music", sfx_dir="assets/sfx"):
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

    def get_audio_mix_filters(self, scene_id, has_impact=False):
        """
        Creates a 'Studio Quality' audio mix.
        - Adds a 50ms fade-in/out to voice to prevent 'pops'.
        - If 'has_impact' is true, it drops the music volume to 0 
          for 200ms before the impact hit.
        """
        voice_filter = "afade=t=in:st=0:d=0.05,afade=t=out:st=duration-0.05:d=0.05"
        music_ducking = "volume=0.15" # Default ducked level
        
        if has_impact:
            # Sidechain 'hole' for the impact SFX
            music_ducking = "volume=0.15:enable='not(between(t,0.4,0.6))',volume=0:enable='between(t,0.4,0.6)'"
            
        return voice_filter, music_ducking
