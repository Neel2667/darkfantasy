import subprocess
import os
import json

class QualityChecker:
    def __init__(self, project_dir="psycho_studio"):
        self.project_dir = project_dir
        self.scene_dir = f"{project_dir}/outputs/scenes"

    def check_video_integrity(self, file_path):
        """Uses ffprobe to check if a video file is corrupted."""
        cmd = [
            'ffprobe', '-v', 'error', 
            '-show_entries', 'format=duration', 
            '-of', 'default=noprint_wrappers=1:nokey=1', 
            file_path
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                return True, float(result.stdout.strip())
            return False, 0
        except Exception:
            return False, 0

    def check_for_black_frames(self, file_path):
        """Detects if a video is mostly black (common rendering error)."""
        # This uses the blackdetect filter in ffmpeg
        cmd = [
            'ffmpeg', '-i', file_path, 
            '-vf', 'blackdetect=d=0.5:pix_th=0.1', 
            '-f', 'null', '-'
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, stderr=subprocess.STDOUT)
            if "black_start" in result.stdout:
                # If black duration is significant, return fail
                return False
            return True
        except Exception:
            return False

    def verify_scene(self, scene_id):
        file_path = f"{self.scene_dir}/scene_{scene_id}.mp4"
        
        print(f"  [QC] Verifying Scene {scene_id}...")
        
        if not os.path.exists(file_path):
            print(f"    ❌ Error: Scene {scene_id} file missing.")
            return False

        # Check integrity
        intact, duration = self.check_video_integrity(file_path)
        if not intact:
            print(f"    ❌ Error: Scene {scene_id} is corrupted.")
            return False
        
        if duration < 0.5:
            print(f"    ❌ Error: Scene {scene_id} is too short ({duration}s).")
            return False

        # Check for black frames
        if not self.check_for_black_frames(file_path):
            print(f"    ⚠️ Warning: Significant black frames detected in Scene {scene_id}.")
            # We might not fail it immediately, but it's a good flag
        
        print(f"    ✅ Scene {scene_id} passed QC.")
        return True

    def run_full_audit(self, scene_ids):
        failed_scenes = []
        for sid in scene_ids:
            if not self.verify_scene(sid):
                failed_scenes.append(sid)
        return failed_scenes
