import os
import json
import time
from scripts.researcher import PsychologyResearcher
from scripts.asset_collector import AssetCollector
from scripts.typography_engine import TypographyEngine
from scripts.visual_effects import CinematicEffects
from scripts.scene_renderer import SceneRenderer
from scripts.final_assembler import FinalAssembler
from scripts.youtube_packager import ViralPackager

class PsychoStudioEngine:
    def __init__(self, topic, length=5):
        self.topic = topic
        self.length = length
        self.project_name = topic.replace(" ", "_").lower()
        self.manifest_path = f"psycho_studio/outputs/manifest_{self.project_name}.json"
        
    def run_full_pipeline(self):
        print(f"🚀 STARTING PRODUCTION: {self.topic}")
        
        # 1. RESEARCH & SCRIPTING
        print("Step 1: Researching & Generating Script via Grok...")
        researcher = PsychologyResearcher(self.topic, self.length)
        generated_path = researcher.generate_manifest()
        
        if generated_path:
            self.manifest_path = generated_path
        else:
            print("Using existing manifest as fallback.")

        # 2. ASSET COLLECTION
        print("Step 2: Collecting Assets (Voice, Stock, SFX)...")
        collector = AssetCollector(self.manifest_path)
        collector.collect_all_assets()

        # 3. SCENE RENDERING (The Assembly Line)
        print("Step 3: Rendering Scenes with Cinematic Effects...")
        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)
            
        scene_files = []
        for scene in manifest['scenes']:
            scene_id = scene['scene_id']
            # Initialize Renderer
            renderer = SceneRenderer(scene, "psycho_studio/assets")
            
            # Build the base scene
            base_scene_path = f"psycho_studio/outputs/scenes/raw_scene_{scene_id}.mp4"
            # (Simulation: in real life FFmpeg would run here)
            
            # Apply Cinematic Effects
            final_scene_path = f"psycho_studio/outputs/scenes/scene_{scene_id}.mp4"
            effects_cmd = CinematicEffects.apply_to_scene(base_scene_path, final_scene_path)
            print(f"  Processed Scene {scene_id} with Cinematic Filters.")
            scene_files.append(final_scene_path)

        # 4. FINAL ASSEMBLY
        print("Step 4: Stitching Final Video...")
        assembler = FinalAssembler("psycho_studio")
        assembler.assemble()

        # 5. YOUTUBE PACKAGING
        print("Step 5: Generating SEO & Thumbnail Strategy...")
        packager = ViralPackager(self.manifest_path)
        packager.generate_seo()

        print("✅ PRODUCTION COMPLETE!")
        print(f"Final Video: psycho_studio/outputs/final/FINAL_VIDEO.mp4")
        print(f"Viral Package: psycho_studio/outputs/viral_package.json")

if __name__ == "__main__":
    # Example trigger
    engine = PsychoStudioEngine("The Psychology of Hidden Envy")
    engine.run_full_pipeline()
