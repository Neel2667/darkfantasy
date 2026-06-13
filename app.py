import gradio as gr
import os
import json
from main import PsychoStudioEngine

def run_studio(topic, length, groq_key, pexels_key):
    # 1. Update config with keys provided in UI (or from Environment Variables)
    config = {
        "api_keys": {
            "groq": groq_key or os.getenv("GROQ_API_KEY"),
            "pexels": pexels_key or os.getenv("PEXELS_API_KEY")
        }
    }
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    # 2. Initialize and Run Engine
    engine = PsychoStudioEngine(topic, length=int(length))
    
    try:
        engine.run_full_pipeline()
        # Paths should be relative to the root of the repo
        video_path = "outputs/final/FINAL_VIDEO.mp4"
        if os.path.exists(video_path):
            return video_path
        else:
            # Check if it's in the subfolder just in case
            alt_path = "psycho_studio/outputs/final/FINAL_VIDEO.mp4"
            if os.path.exists(alt_path):
                return alt_path
            return f"Error: Video not found. Checked {video_path} and {alt_path}"
    except Exception as e:
        return f"Error during production: {str(e)}"

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🧠 PSYCHO STUDIO AI")
    gr.Markdown("### Fully Autonomous Dark Psychology Video Factory")
    
    with gr.Row():
        with gr.Column():
            topic = gr.Textbox(label="Video Topic", placeholder="e.g., The Psychology of Silent Manipulation")
            length = gr.Slider(minimum=1, maximum=15, value=5, step=1, label="Target Length (Minutes)")
            
            gr.Markdown("#### API Keys (Leave blank if using Space Secrets)")
            groq_k = gr.Textbox(label="Groq Key", type="password")
            pexels_k = gr.Textbox(label="Pexels Key", type="password")
            
            btn = gr.Button("🚀 START PRODUCTION", variant="primary")
            
        with gr.Column():
            output_video = gr.Video(label="Generated Masterpiece")

    btn.click(fn=run_studio, inputs=[topic, length, groq_k, pexels_k], outputs=output_video)

# Hugging Face requires server_name="0.0.0.0" and server_port=7860
demo.launch(server_name="0.0.0.0", server_port=7860, theme=gr.themes.Soft())
