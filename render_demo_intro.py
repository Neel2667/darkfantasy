import os
import subprocess
from scripts.intro_engine import IntroEngine

def render_elite_intro_demo():
    print("🎬 RENDERING ELITE CHAPTER INTRO DEMO...")
    
    # 0. Setup
    os.makedirs("outputs/scenes", exist_ok=True)
    engine = IntroEngine()
    
    # Use the demo clip
    input_video = "assets/stock/demo_clip.mp4"
    output_video = "outputs/scenes/ELITE_INTRO_DEMO.mp4"
    chapter_text = "THE ANATOMY OF FEAR"
    
    if not os.path.exists(input_video):
        print("❌ Demo failed: Input stock video missing.")
        return

    # 1. Apply Template 02: The Blueprint HUD
    print(f"Applying Template 02 (Blueprint HUD) to: {chapter_text}")
    cmd = engine.apply_blueprint_hud(chapter_text, input_video, output_video)
    
    # Add path to ffmpeg
    cmd[0] = "/home/user/ffmpeg_bin/ffmpeg"
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ ELITE INTRO RENDERED: {output_video}")
    except Exception as e:
        print(f"❌ Render Error: {e}")

if __name__ == "__main__":
    render_elite_intro_demo()
