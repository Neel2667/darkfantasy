import subprocess
import os

class CinematicEffects:
    @staticmethod
    def get_complex_filter(zoom=True, grain=True, color_grade=True):
        filters = []
        
        # 1. Ken Burns Effect (Slow Zoom)
        if zoom:
            # Zooms into the center slightly over time
            filters.append("zoompan=z='min(zoom+0.0015,1.5)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080")

        # 2. Cinematic Color Grading
        if color_grade:
            # eq: contrast, brightness, saturation, gamma
            # colorchannelmixer: Tints the shadows blue and highlights slightly warm
            filters.append("eq=contrast=1.15:brightness=-0.05:saturation=0.8:gamma=0.9")
            filters.append("colorchannelmixer=rr=1.0:rb=0.1:br=0.1:bb=1.1") 

        # 3. Vignette (Darkens edges to focus on center)
        filters.append("vignette=angle=PI/4:x0=w/2:y0=h/2")

        # 4. Film Grain (Fine noise overlay)
        if grain:
            filters.append("noise=alls=10:allf=t+u")

        return ",".join(filters)

    @staticmethod
    def apply_to_scene(input_path, output_path):
        filter_str = CinematicEffects.get_complex_filter()
        
        cmd = [
            'ffmpeg', '-y',
            '-i', input_path,
            '-vf', filter_str,
            '-c:v', 'libx264',
            '-crf', '18', # High quality
            '-preset', 'slow',
            output_path
        ]
        return cmd

# Example usage logic for the pipeline
if __name__ == "__main__":
    print("Cinematic Effects Engine Loaded.")
