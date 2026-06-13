import os
import json

from scripts.api_client import APIClient

class AssetCollector:
    def __init__(self, manifest_path):
        with open(manifest_path, 'r') as f:
            self.manifest = json.load(f)
        self.client = APIClient()
            
    def collect_all_assets(self):
        print(f"Starting Asset Collection for: {self.manifest['metadata']['title']}")
        
        for scene in self.manifest['scenes']:
            scene_id = scene['scene_id']
            print(f"--- Processing Scene {scene_id} ---")
            
            # 1. Voiceover
            voice_path = f"assets/voice/scene_{scene_id}.mp3"
            if not os.path.exists(voice_path):
                self.client.generate_voice(scene['narration'], voice_path)
            
            # 2. Stock Footage (Downloading 3 clips per scene for 2-3s pacing)
            for i in range(3):
                stock_path = f"assets/stock/scene_{scene_id}_{i}.mp4"
                if not os.path.exists(stock_path) and len(scene['visual_queries']) > i:
                    query = scene['visual_queries'][i]
                    print(f"  [STOCK] Downloading shot {i} for scene {scene_id}...")
                    self.client.download_pexels_video(query, stock_path)

        # 3. Thumbnail Background
        thumb_bg = "assets/stock/thumb_bg.jpg"
        if not os.path.exists(thumb_bg):
            print("--- Fetching Thumbnail Background ---")
            # Grok usually provides visual_queries in the first scene that are good for thumbs
            query = self.manifest['scenes'][0]['visual_queries'][0] + " dramatic"
            self.client.download_pexels_photo(query, thumb_bg)

if __name__ == "__main__":
    collector = AssetCollector("psycho_studio/outputs/mock_manifest.json")
    collector.collect_all_assets()
