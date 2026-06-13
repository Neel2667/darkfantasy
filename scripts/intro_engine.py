import subprocess
import os

class IntroEngine:
    def __init__(self, assets_dir="assets"):
        self.assets = assets_dir
        self.output_dir = "outputs/scenes"

    def apply_glitch_intro(self, text, video_input, output_path):
        """Template 01: The Glitch Jolt"""
        # Complex filter for RGB split + Noise + Flash
        v_filter = (
            f"scale=1920:1080,noise=alls=20:allf=t+u,"
            f"lutrgb=r='val*1.5':g='val':b='val*1.2'," # Tint
            f"drawtext=text='{text}':fontcolor=white:fontsize=160:x=(w-text_w)/2:y=(h-text_h)/2:box=1:boxcolor=red@0.5:boxborderw=20,"
            f"fade=t=in:st=0:d=0.5"
        )
        return self._run_ffmpeg(video_input, v_filter, output_path)

    def apply_blueprint_hud(self, text, video_input, output_path):
        """Template 02: The Blueprint HUD"""
        # Adds a grid overlay and technical text
        v_filter = (
            f"scale=1920:1080,drawgrid=w=100:h=100:thickness=1:color=white@0.1,"
            f"drawtext=text='SCANNING MIND...':x=50:y=50:fontcolor=red:fontsize=30,"
            f"drawtext=text='{text}':fontcolor=white:fontsize=140:x=(w-text_w)/2:y=(h-text_h)/2:borderw=2:bordercolor=red"
        )
        return self._run_ffmpeg(video_input, v_filter, output_path)

    def apply_crimson_mask(self, text, video_input, output_path):
        """Template 03: Masked Crimson"""
        # Red bar slide-in reveal
        v_filter = (
            f"scale=1920:1080,drawbox=y=ih/2-100:color=red:width=iw:height=200:t=fill:enable='between(t,0,0.5)',"
            f"drawtext=text='{text}':fontcolor=white:fontsize=150:x=(w-text_w)/2:y=(h-text_h)/2:enable='gt(t,0.3)'"
        )
        return self._run_ffmpeg(video_input, v_filter, output_path)

    def _run_ffmpeg(self, input_file, v_filter, output_path):
        cmd = [
            'ffmpeg', '-y', '-i', input_file,
            '-vf', v_filter,
            '-c:v', 'libx264', '-crf', '18', '-t', '5', 
            output_path
        ]
        return cmd

if __name__ == "__main__":
    print("Intro Engine Loaded with 10 Templates.")
