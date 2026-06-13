import json

class ViralPackager:
    def __init__(self, manifest_path):
        with open(manifest_path, 'r') as f:
            self.manifest = json.load(f)
            
    def generate_seo(self):
        # We use the topic and metadata to create high-retention titles
        original_title = self.manifest['metadata']['title']
        
        seo_data = {
            "titles": [
                f"The Dark Side of {original_title}: 3 Tricks to Master It",
                f"Why {original_title} is Ruining Your Life (Psychology)",
                f"How to Use {original_title} to Control Any Conversation",
                f"The SCARY Truth About {original_title}"
            ],
            "thumbnail_logic": {
                "background": "High contrast, dark, blurry silhouettes",
                "center_object": "A single red object (e.g., a glowing eye, a red string, a bloody chess piece)",
                "text_overlay": "DON'T LOOK AWAY",
                "emotions": "Fear, Curiosity, Urgency"
            },
            "description_hook": "Most people think they are in control. They are wrong. In this video, we dive into the dark mechanics of...",
            "tags": ["Dark Psychology", "Manipulation", "Social Skills", "Human Behavior", "Gen Z Psychology", "Mind Games"]
        }
        
        path = "outputs/viral_package.json"
        with open(path, 'w') as f:
            json.dump(seo_data, f, indent=4)
        return path

if __name__ == "__main__":
    print("Viral Packager Ready.")
