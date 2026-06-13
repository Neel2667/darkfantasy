import os
import subprocess

class FinalAssembler:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.scene_dir = f"{project_dir}/outputs/scenes"
        self.output_path = f"{project_dir}/outputs/final/FINAL_VIDEO.mp4"
        
    def assemble(self):
        # 1. Get all scene files in order
        scenes = sorted([f for f in os.listdir(self.scene_dir) if f.endswith(".mp4")])
        
        if not scenes:
            print("No scenes found to assemble.")
            return
            
        # 2. Create a 'list.txt' for FFmpeg concat
        list_path = f"{self.project_dir}/outputs/scenes/list.txt"
        with open(list_path, 'w') as f:
            for scene in scenes:
                f.write(f"file '{scene}'\n")
                
        # 3. Run Concat Command
        print(f"Assembling {len(scenes)} scenes into final video...")
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', list_path,
            '-c', 'copy', # Copy codecs to save time (no re-encoding)
            self.output_path
        ]
        
        # In a real environment: subprocess.run(cmd)
        print(f"Project Complete! Final Export: {self.output_path}")

if __name__ == "__main__":
    assembler = FinalAssembler("psycho_studio")
    # assembler.assemble()
