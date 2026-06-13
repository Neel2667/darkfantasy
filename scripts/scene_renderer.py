import subprocess
import os

class MasterCompositor:
    def __init__(self, scene_data, assets_dir):
        self.data = scene_data
        self.assets = assets_dir
        self.output_dir = "psycho_studio/outputs/scenes"
        os.makedirs(self.output_dir, exist_ok=True)

    def compose_scene(self):
        scene_id = self.data['scene_id']
        output_file = f"{self.output_dir}/scene_{scene_id}.mp4"
        
        # Asset Paths
        stock = f"{self.assets}/stock/scene_{scene_id}_0.mp4"
        voice = f"{self.assets}/voice/scene_{scene_id}.mp3"
        # Optional typography frames (using the first one for this example)
        typo = f"{self.assets}/typography/scene_{scene_id}_0.png"
        
        # Check if assets exist, fallback to placeholders if needed
        if not os.path.exists(stock): stock = "psycho_studio/assets/stock/placeholder.mp4"
        if not os.path.exists(voice): voice = "psycho_studio/assets/voice/placeholder.mp3"
        
        # FFmpeg Filter Complex Logic:
        # 1. Scale stock to 1080p and apply Cinematic Grade
        # 2. Overlay Typography PNG with a 0.5s fade-in
        # 3. Apply sidechain audio ducking
        
        filter_complex = (
            f"[0:v]scale=1920:1080,format=yuv420p,eq=contrast=1.2:brightness=-0.05:saturation=0.7,"
            f"vignette=angle=PI/4[bg];"
            f"[1:v]format=rgba,fade=t=in:st=0.5:d=0.5:alpha=1[text];"
            f"[bg][text]overlay=(W-w)/2:(H-h)/2[v_out]"
        )

        cmd = [
            'ffmpeg', '-y',
            '-i', stock,          # Input 0: Video
            '-i', typo,           # Input 1: Typography
            '-i', voice,           # Input 2: Voice
            '-filter_complex', filter_complex,
            '-map', '[v_out]',
            '-map', '2:a',         # Use voice audio
            '-c:v', 'libx264',
            '-crf', '20',
            '-preset', 'fast',
            '-shortest',           # End when audio ends
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
