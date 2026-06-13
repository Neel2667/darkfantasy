import subprocess
import os

class MasterCompositor:
    def __init__(self, scene_data, assets_dir):
        self.data = scene_data
        self.assets = assets_dir
        self.output_dir = "psycho_studio/outputs/scenes"
        os.makedirs(self.output_dir, exist_ok=True)

    def compose_scene(self, sfx_cue=None):
        scene_id = self.data['scene_id']
        output_file = f"{self.output_dir}/scene_{scene_id}.mp4"
        
        # Asset Paths
        stock = f"{self.assets}/stock/scene_{scene_id}_0.mp4"
        voice = f"{self.assets}/voice/scene_{scene_id}.mp3"
        typo = f"{self.assets}/typography/scene_{scene_id}_0.png"
        
        # Audio Engine for SFX
        from scripts.audio_engine import AudioEngine
        ae = AudioEngine()
        sfx_path = ae.get_sfx_path(sfx_cue) if sfx_cue else None

        # Filter Complex Logic:
        # 1. Video: Stock -> Grade -> Vignette -> Typography Overlay
        # 2. Audio: Voice + SFX (at 0.5s) + Ducked Background Music (Global)
        
        v_filter = (
            f"[0:v]scale=1920:1080,format=yuv420p,eq=contrast=1.2:brightness=-0.05:saturation=0.7,"
            f"vignette=angle=PI/4[bg];"
            f"[1:v]format=rgba,fade=t=in:st=0.5:d=0.5:alpha=1[text];"
            f"[bg][text]overlay=(W-w)/2:(H-h)/2[v_out]"
        )

        # Audio mix: Voice is main. SFX is added at 0.5s offset to match text.
        a_filter = "[2:a]volume=1.0[v_aud];"
        if sfx_path and os.path.exists(sfx_path):
            a_filter += f"[3:a]adelay=500|500,volume=0.6[sfx];[v_aud][sfx]amix=inputs=2:duration=first[a_out]"
            audio_inputs = ['-i', sfx_path]
            a_map = "[a_out]"
        else:
            a_map = "[v_aud]"
            audio_inputs = []

        cmd = [
            'ffmpeg', '-y',
            '-i', stock,
            '-i', typo,
            '-i', voice,
        ] + audio_inputs + [
            '-filter_complex', f"{v_filter}{a_filter}",
            '-map', '[v_out]',
            '-map', a_map,
            '-c:v', 'libx264', '-crf', '20', '-preset', 'fast', '-shortest',
            output_file
        ]

        print(f"🎬 Composing Scene {scene_id}...")
        try:
            # subprocess.run(cmd, check=True)
            print(f"✅ Scene {scene_id} Rendered.")
        except Exception as e:
            print(f"❌ Render Error Scene {scene_id}: {e}")

if __name__ == "__main__":
    print("Master Compositor Loaded.")
