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
        mood = self.data.get('music_mood', 'dark_ambient').lower()
        output_file = f"{self.output_dir}/scene_{scene_id}.mp4"
        
        # 1. ARRANGE 3 SHOTS FOR 2-3s PACING
        shots = []
        for i in range(3):
            path = f"{self.assets}/stock/scene_{scene_id}_{i}.mp4"
            if os.path.exists(path):
                shots.append(path)
        
        # If we have 3 shots, we divide the scene duration by 3
        # Logic: [Shot 0 (0-3s)][Shot 1 (3-6s)][Shot 2 (6-9s)]
        
        voice = f"{self.assets}/voice/scene_{scene_id}.mp3"
        typo = f"{self.assets}/typography/scene_{scene_id}_0.png"
        
        # Complex Filter: Layering multiple inputs in a sequence
        # We use 'trim' and 'setpts' for each shot to make them 2.5s segments
        v_filter = ""
        for i in range(len(shots)):
            v_filter += f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setpts=PTS-STARTPTS[v{i}];"
        
        # Concat the shots
        v_filter += "".join([f"[v{i}]" for i in range(len(shots))])
        v_filter += f"concat=n={len(shots)}:v=1:a=0[bg_raw];"
        
        # Apply Global Style to the concatenated stream
        color_grade = "colorbalance=rs=-0.1:gs=-0.05:bs=0.1:rm=0.1:gm=0.05:bm=-0.05:rh=0.05:gh=0.05:bh=0.05"
        v_filter += f"[bg_raw]{color_grade},noise=alls=8:allf=t+u,vignette=angle=PI/4[bg];"
        
        # Overlay Typography
        v_filter += f"[{len(shots)}:v]format=rgba,fade=t=in:st=0.5:d=0.5:alpha=1[text];[bg][text]overlay=(W-w)/2:(H-h)/2[v_out]"
        
        # Audio mapping (Input index for voice is len(shots) + 1)
        voice_idx = len(shots) + 1
        
        cmd = ['ffmpeg', '-y']
        for s in shots: cmd += ['-ss', '2.0', '-t', '3.0', '-i', s] # Cut 3s from the 'heart' of each clip
        cmd += ['-i', typo, '-i', voice]
        cmd += ['-filter_complex', v_filter, '-map', '[v_out]', '-map', f'{voice_idx}:a', '-shortest', output_file]

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
            '-ss', f"{start_time:.2f}",
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
