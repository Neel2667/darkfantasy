import subprocess
import os

class MasterCompositor:
    def __init__(self, scene_data, assets_dir):
        self.data = scene_data
        self.assets = assets_dir
        self.output_dir = "outputs/scenes"
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
            elif i == 0:
                # Fallback to a placeholder if at least the first one is missing
                shots.append("assets/stock/placeholder.mp4")
        
        voice = f"{self.assets}/voice/scene_{scene_id}.mp3"
        typo = f"{self.assets}/typography/scene_{scene_id}_0.png"
        
        # Audio Engine for SFX
        from scripts.audio_engine import AudioEngine
        ae = AudioEngine()
        sfx_path = ae.get_sfx_path(sfx_cue) if sfx_cue else None

        # Filter Complex Logic for Video:
        # Layering multiple inputs in a sequence
        v_filter = ""
        for i in range(len(shots)):
            # Scale and crop each shot
            v_filter += f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setpts=PTS-STARTPTS[v{i}];"
        
        # Concat the shots
        v_filter += "".join([f"[v{i}]" for i in range(len(shots))])
        v_filter += f"concat=n={len(shots)}:v=1:a=0[bg_raw];"
        
        # Apply Global Style (Color Grade, Noise, Vignette, Bloom)
        color_grade = "colorbalance=rs=-0.1:gs=-0.05:bs=0.1:rm=0.1:gm=0.05:bm=-0.05:rh=0.05:gh=0.05:bh=0.05"
        bloom = "split[a][b];[b]boxblur=10:1[b_blur];[a][b_blur]blend=all_mode='screen':all_opacity=0.15"
        v_filter += f"[bg_raw]{bloom},{color_grade},noise=alls=8:allf=t+u,vignette=angle=PI/4[bg];"
        
        # Overlay Typography
        typo_idx = len(shots)
        v_filter += f"[{typo_idx}:v]format=rgba,fade=t=in:st=0.5:d=0.5:alpha=1[text];[bg][text]overlay=(W-w)/2:(H-h)/2[v_out];"
        
        # Audio mix: Voice is main. SFX is added at 0.5s offset.
        voice_idx = len(shots) + 1
        sfx_idx = len(shots) + 2
        
        a_filter = f"[{voice_idx}:a]volume=1.0[v_aud];"
        audio_inputs = []
        if sfx_path and os.path.exists(sfx_path):
            a_filter += f"[{sfx_idx}:a]adelay=500|500,volume=0.6[sfx_ch];[v_aud][sfx_ch]amix=inputs=2:duration=first[a_out]"
            audio_inputs = ['-i', sfx_path]
            a_map = "[a_out]"
        else:
            a_map = "[v_aud]"

        cmd = ['ffmpeg', '-y']
        # Add Shots (Seeked to heart)
        for s in shots:
            cmd += ['-ss', '2.0', '-t', '3.0', '-i', s]
        
        # Add Typography
        cmd += ['-i', typo]
        # Add Voice
        cmd += ['-i', voice]
        # Add SFX if exists
        cmd += audio_inputs
        
        # Add Filters
        cmd += [
            '-filter_complex', v_filter + a_filter,
            '-map', '[v_out]',
            '-map', a_map,
            '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-shortest',
            output_file
        ]

        print(f"🎬 Composing Scene {scene_id}...")
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ Scene {scene_id} Rendered.")
        except Exception as e:
            print(f"❌ Render Error Scene {scene_id}: {e}")

if __name__ == "__main__":
    print("Master Compositor Loaded.")
