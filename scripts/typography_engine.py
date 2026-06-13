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

    def create_masked_text(self, text, output_path):
        """
        Creates text designed for a 'Mask Reveal' (e.g., behind a wall)
        """
        # This usually involves creating a high-contrast alpha mask
        self.create_text_frame(text, output_path, color="#FFFFFF")
        print(f"      [TYPO] Created Masking Frame for: '{text}'")

if __name__ == "__main__":
    engine = TypographyEngine()
    os.makedirs("psycho_studio/assets/typography", exist_ok=True)
    engine.create_text_frame("DARK PSYCHOLOGY", "psycho_studio/assets/typography/test.png")
