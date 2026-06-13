import os
import json
import asyncio
import edge_tts
import requests
from scripts.researcher import PsychologyResearcher
from scripts.asset_collector import AssetCollector
from scripts.typography_engine import TypographyEngine
from scripts.scene_renderer import MasterCompositor
from scripts.final_assembler import FinalAssembler
from scripts.youtube_packager import ViralPackager

async def generate_5min_video(topic, groq_key, pexels_key):
    print(f"🚀 INITIALIZING 5-MINUTE PRODUCTION: {topic}")
    
    # 0. Setup Environment
    os.makedirs("outputs/scenes", exist_ok=True)
    os.makedirs("outputs/final", exist_ok=True)
    os.makedirs("assets/voice", exist_ok=True)
    os.makedirs("assets/stock", exist_ok=True)
    os.makedirs("assets/typography", exist_ok=True)
    
    config = {
        "api_keys": {
            "groq": groq_key,
            "pexels": pexels_key
        }
    }
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    # 1. RESEARCH (Script Generation)
    print("\n--- STEP 1: GENERATING SCRIPT ---")
    researcher = PsychologyResearcher(topic, length_minutes=5)
    manifest_path = researcher.generate_manifest()
    
    if not manifest_path or not os.path.exists(manifest_path):
        print("❌ Failed to generate script manifest.")
        return

    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    # 2. ASSETS (Voice & Stock)
    print("\n--- STEP 2: COLLECTING ASSETS ---")
    collector = AssetCollector(manifest_path)
    collector.collect_all_assets()

    # 3. TYPOGRAPHY (Generating Text Overlays)
    print("\n--- STEP 3: GENERATING TYPOGRAPHY ---")
    typo_engine = TypographyEngine()
    for scene in manifest['scenes']:
        text = scene['on_screen_text'][0] if scene['on_screen_text'] else "PSYCHO STUDIO"
        output_path = f"assets/typography/scene_{scene['scene_id']}_0.png"
        typo_engine.create_text_frame(text, output_path)

    # 4. RENDERING (Scene by Scene)
    print("\n--- STEP 4: RENDERING SCENES ---")
    for scene in manifest['scenes']:
        renderer = MasterCompositor(scene, "assets")
        renderer.compose_scene(sfx_cue=scene.get('sfx_cue', 'whoosh'))

    # 5. ASSEMBLY
    print("\n--- STEP 5: FINAL ASSEMBLY ---")
    assembler = FinalAssembler(".")
    assembler.assemble()

    # 6. PACKAGING
    print("\n--- STEP 6: SEO & THUMBNAIL ---")
    packager = ViralPackager(manifest_path)
    packager.generate_seo()
    
    print("\n✅ PRODUCTION COMPLETE!")
    print(f"Final Video: outputs/final/FINAL_VIDEO.mp4")

if __name__ == "__main__":
    # You must provide your GROQ key here to run it in this environment
    # Or run it via the Dashboard on Hugging Face using the provided Pexels key.
    TOPIC = "The Psychology of Silent Manipulation: Why Silence is Your Deadliest Weapon"
    GROQ_KEY = "PASTE_YOUR_GROQ_KEY_HERE"
    PEXELS_KEY = "VSVVwVr2PbdZwEC2CBEppyAgqU7ke5PJRPnRfTKHwnis7B4xXGKKhEr8"
    
    # asyncio.run(generate_5min_video(TOPIC, GROQ_KEY, PEXELS_KEY))
    print("Script ready. Please paste your Groq key into the main block and run or use the Dashboard.")
