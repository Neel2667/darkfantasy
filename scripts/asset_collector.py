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
            voice_path = f"psycho_studio/assets/voice/scene_{scene_id}.mp3"
            if not os.path.exists(voice_path):
                self.client.generate_elevenlabs_voice(scene['narration'], voice_path)
            
            # 2. Stock Footage (Downloading first visual query)
            stock_path = f"psycho_studio/assets/stock/scene_{scene_id}_0.mp4"
            if not os.path.exists(stock_path) and scene['visual_queries']:
                query = scene['visual_queries'][0]
                self.client.download_pexels_video(query, stock_path)

if __name__ == "__main__":
    collector = AssetCollector("psycho_studio/outputs/mock_manifest.json")
    collector.collect_all_assets()
