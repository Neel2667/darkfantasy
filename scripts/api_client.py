import requests
import json
import os
import asyncio
import edge_tts

class APIClient:
    def __init__(self, config_path="config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.keys = self.config['api_keys']

    def call_groq(self, prompt):
        """
        Calls Groq API (FREE Tier available)
        Model: llama-3.3-70b-versatile
        """
        api_key = self.keys.get('groq') or os.getenv("GROQ_API_KEY")
        url = "https://api.groq.com/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a professional video script architect. Output ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            content = response.json()['choices'][0]['message']['content']
            return json.loads(content)
        except Exception as e:
            print(f"Error calling Groq: {e}")
            return None

    def download_pexels_video(self, query, output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        url = "https://api.pexels.com/videos/search"
        # ...
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
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
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
