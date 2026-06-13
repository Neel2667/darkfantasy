import requests
import json
import os
import asyncio
import edge_tts

class APIClient:
    def __init__(self, config_path="psycho_studio/config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.keys = self.config['api_keys']

    def call_free_llm(self, prompt):
        """
        Calls Hugging Face Inference API (FREE)
        Model: Qwen/Qwen2.5-72B-Instruct or Llama-3-70B
        """
        # HF_TOKEN can be found in Hugging Face settings (Free)
        # On a HF Space, it's often provided automatically as an env var.
        hf_token = self.keys.get('huggingface') or os.getenv("HF_TOKEN")
        
        API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct"
        headers = {"Authorization": f"Bearer {hf_token}"}
        
        payload = {
            "inputs": f"<|system|>\nYou are a professional video script architect. Output ONLY valid JSON.\n<|user|>\n{prompt}\n<|assistant|>\n",
            "parameters": {"max_new_tokens": 4000, "return_full_text": False}
        }
        
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            content = response.json()[0]['generated_text']
            
            # Clean JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            return json.loads(content)
        except Exception as e:
            print(f"Error calling Free LLM: {e}")
            return None

    def download_pexels_video(self, query, output_path):
        url = "https://api.pexels.com/videos/search"
        headers = {"Authorization": self.keys['pexels']}
        params = {"query": query, "per_page": 1, "orientation": "landscape"}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if data['videos']:
                video_files = data['videos'][0]['video_files']
                link = next((f['link'] for f in video_files if f['width'] == 1920), video_files[0]['link'])
                vid_data = requests.get(link).content
                with open(output_path, 'wb') as f:
                    f.write(vid_data)
                return True
        except Exception as e:
            print(f"Error downloading Pexels video: {e}")
        return False

    def generate_voice(self, text, output_path):
        """Edge-TTS is 100% Free"""
        voice = "en-US-ChristopherNeural" 
        async def _save():
            communicate = edge_tts.Communicate(text, voice, rate="+0%", pitch="-5Hz")
            await communicate.save(output_path)
        try:
            asyncio.run(_save())
            return True
        except Exception as e:
            print(f"Error with Edge TTS: {e}")
            return False
