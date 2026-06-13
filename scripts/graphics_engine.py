from PIL import Image, ImageDraw, ImageFont
import os

class GraphicsEngine:
    def __init__(self, theme="dark"):
        self.canvas_size = (1920, 1080)
        self.bg_color = (0, 0, 0, 0) # Transparent
        self.accent_color = (255, 0, 0, 255) # Dark Psychology Red
        self.text_color = (255, 255, 255, 255)

    def create_stat_bar(self, label, percentage, output_path):
        """Creates a minimalist bar chart for a statistic (e.g., '95% of people fail')"""
        img = Image.new('RGBA', self.canvas_size, self.bg_color)
        draw = ImageDraw.Draw(img)
        
        # Draw Label
        # draw.text((500, 400), label, fill=self.text_color, font=font)
        
        # Draw Bar Background
        bar_x, bar_y = 460, 540
        bar_w, bar_h = 1000, 40
        draw.rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], fill=(50, 50, 50, 255))
        
        # Draw Filled Bar
        fill_w = (percentage / 100) * bar_w
        draw.rectangle([bar_x, bar_y, bar_x + fill_w, bar_y + bar_h], fill=self.accent_color)
        
        # Draw Percentage Text
        # draw.text((bar_x + fill_w + 20, bar_y - 20), f"{percentage}%", fill=self.text_color)
        
        img.save(output_path)
        print(f"      [GRAPHIC] Created Stat Bar: {label} ({percentage}%)")

if __name__ == "__main__":
    engine = GraphicsEngine()
    os.makedirs("psycho_studio/assets/graphics", exist_ok=True)
    engine.create_stat_bar("MANIPULATION SUCCESS", 87, "psycho_studio/assets/graphics/test_stat.png")
