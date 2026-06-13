from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os
import json

class ThumbnailGenerator:
    def __init__(self, assets_dir="psycho_studio/assets", output_dir="psycho_studio/outputs/final"):
        self.assets_dir = assets_dir
        self.output_dir = output_dir
        self.canvas_size = (1280, 720) # YouTube Standard
        os.makedirs(self.output_dir, exist_ok=True)

    def create_thumbnail(self, title_text, bg_image_path, output_name="Thumbnail.png"):
        """
        Creates a high-contrast, dark-psychology style thumbnail.
        """
        print(f"🎨 Generating Thumbnail: {title_text}")
        
        # 1. Load Background
        if os.path.exists(bg_image_path):
            bg = Image.open(bg_image_path).convert("RGBA")
            bg = bg.resize(self.canvas_size, Image.Resampling.LANCZOS)
        else:
            # Fallback to solid black if no image provided
            bg = Image.new("RGBA", self.canvas_size, (10, 10, 15, 255))

        # 2. Apply "Dark & Moody" Grade
        # Darken it significantly to make text pop
        enhancer = ImageEnhance.Brightness(bg)
        bg = enhancer.enhance(0.4)
        # Apply a slight blur to create depth
        bg = bg.filter(ImageFilter.GaussianBlur(radius=3))

        # 3. Create Text Layer
        text_layer = Image.new("RGBA", self.canvas_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)
        
        # Attempt to load a bold font
        try:
            # You would place a bold .ttf in your assets/fonts
            font = ImageFont.truetype("psycho_studio/assets/fonts/Montserrat-ExtraBold.ttf", 140)
        except:
            font = ImageFont.load_default()

        # Split text into lines if too long
        words = title_text.upper().split()
        lines = [" ".join(words[:len(words)//2]), " ".join(words[len(words)//2:])] if len(words) > 3 else [" ".join(words)]

        # 4. Draw Text with "Glow/Shadow"
        y_offset = 200
        for line in lines:
            # Draw shadow
            draw.text((64, y_offset + 4), line, font=font, fill=(0, 0, 0, 200))
            # Draw main text (White or Yellow for contrast)
            draw.text((60, y_offset), line, font=font, fill=(255, 255, 255, 255))
            y_offset += 160

        # 5. Add "The Red Accent" (Psychological Trigger)
        # Add a red border or a glowing red dot/line
        draw.rectangle([0, 0, 20, 720], fill=(255, 0, 0, 255)) # Red left border

        # 6. Combine and Save
        final_thumb = Image.alpha_composite(bg, text_layer)
        output_path = f"{self.output_dir}/{output_name}"
        final_thumb.convert("RGB").save(output_path, "PNG")
        
        print(f"✅ Thumbnail saved to {output_path}")
        return output_path

if __name__ == "__main__":
    # Test
    gen = ThumbnailGenerator()
    # gen.create_thumbnail("DON'T LOOK AWAY", "psycho_studio/assets/stock/test_bg.jpg")
