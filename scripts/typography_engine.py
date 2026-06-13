from PIL import Image, ImageDraw, ImageFont
import os

class TypographyEngine:
    def __init__(self, font_path=None):
        # Default to a bold sans-serif
        self.font_path = font_path # User would provide a .ttf path
        self.canvas_size = (1920, 1080)
        
    def create_glitch_text(self, text, output_dir, scene_id):
        """
        Creates a series of frames for a glitch reveal effect.
        """
        os.makedirs(output_dir, exist_ok=True)
        # Create 5 frames with slight offsets and color shifts
        for i in range(5):
            img = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype(self.font_path, 160)
            except:
                font = ImageFont.load_default()
            
            # Random offset for glitch
            offset = (i % 2 * 10, i % 3 * 5)
            # Alternate colors (Red/Cyan glitch)
            color = (255, 0, 0, 200) if i % 2 == 0 else (0, 255, 255, 200)
            
            draw.text((self.canvas_size[0]//2 + offset[0], self.canvas_size[1]//2 + offset[1]), 
                      text, font=font, fill=color, anchor="mm")
            
            frame_path = f"{output_dir}/glitch_{scene_id}_{i}.png"
            img.save(frame_path)
        print(f"      [TYPO] Created Glitch Frames for: '{text}'")

    def create_momentum_typography(self, text, output_dir, scene_id, duration_frames=30):
        """
        GSAP-Inspired Motion:
        Uses an 'Elastic' or 'Back' ease-out function for the text scaling.
        This creates the 'High-End Studio' feel where text bounces slightly.
        """
        os.makedirs(output_dir, exist_ok=True)
        for i in range(duration_frames):
            t = i / duration_frames
            # 'Back Ease Out' formula
            c1 = 1.70158
            c3 = c1 + 1
            ease_back_out = 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)
            
            scale = 0.5 + (0.5 * ease_back_out) # Starts at 0.5, ends at 1.0 with a bounce
            opacity = int(255 * min(1, t * 2))

            img = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            # ... render with scale ...

    def create_text_frame(self, text, output_path, color="#FFFFFF"):
        # Create a transparent background
        img = Image.new('RGBA', self.canvas_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype(self.font_path, 150)
        except:
            font = ImageFont.load_default()
        draw.text((self.canvas_size[0]//2, self.canvas_size[1]//2), 
                  text, font=font, fill=color, anchor="mm")
        img.save(output_path)
        print(f"      [TYPO] Created frame for: '{text}' at {output_path}")

if __name__ == "__main__":
    engine = TypographyEngine()
    os.makedirs("psycho_studio/assets/typography", exist_ok=True)
    engine.create_text_frame("DARK PSYCHOLOGY", "psycho_studio/assets/typography/test.png")
