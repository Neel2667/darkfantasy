import os
import json
import time
from scripts.researcher import PsychologyResearcher
from scripts.asset_collector import AssetCollector
from scripts.typography_engine import TypographyEngine
from scripts.visual_effects import CinematicEffects
from scripts.scene_renderer import MasterCompositor
from scripts.final_assembler import FinalAssembler
from scripts.youtube_packager import ViralPackager

class PsychoStudioEngine:
    def __init__(self, topic, length=5):
        self.topic = topic
        self.length = length
        self.project_name = topic.replace(" ", "_").lower()
        self.manifest_path = f"psycho_studio/outputs/manifest_{self.project_name}.json"
        
from scripts.quality_checker import QualityChecker

class PsychoStudioEngine:
    # ... previous code ...
    
    def run_full_pipeline(self):
        # ... Steps 1 & 2 ...

        # 3. SCENE RENDERING
        print("Step 3: Rendering Scenes & Quality Control...")
        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)
            
        qc = QualityChecker("psycho_studio")
        scene_ids = [s['scene_id'] for s in manifest['scenes']]
        
        for scene in manifest['scenes']:
            renderer = MasterCompositor(scene, "psycho_studio/assets")
            renderer.compose_scene(sfx_cue=scene.get('sfx_cue'))
            
            # Immediate QC
            if not qc.verify_scene(scene['scene_id']):
                print(f"  ⚠️ Scene {scene['scene_id']} failed QC. Attempting one re-render...")
                renderer.compose_scene(sfx_cue=scene.get('sfx_cue'))

        # 4. FINAL ASSEMBLY
        # ...
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
