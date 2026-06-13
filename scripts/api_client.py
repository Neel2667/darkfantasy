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

    def call_grok(self, prompt):
        """Calls the Grok/X.AI API"""
        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.keys['grok']}"
        }
        data = {
            "model": "grok-beta",
            "messages": [
                {"role": "system", "content": "You are a professional video script architect."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            content = response.json()['choices'][0]['message']['content']
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            return json.loads(content)
        except Exception as e:
            print(f"Error calling Grok: {e}")
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

    def download_pexels_photo(self, query, output_path):
        url = "https://api.pexels.com/v1/search"
        headers = {"Authorization": self.keys['pexels']}
        params = {"query": query, "per_page": 1}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if data['photos']:
                link = data['photos'][0]['src']['large2x']
                photo_data = requests.get(link).content
                with open(output_path, 'wb') as f:
                    f.write(photo_data)
                return True
        except Exception as e:
            print(f"Error downloading Pexels photo: {e}")
        return False

    def generate_voice(self, text, output_path):
        """Generates voiceover using Edge TTS (High Quality, Free)"""
        # Deep, cinematic voice: en-US-ChristopherNeural or en-GB-RyanNeural
        voice = "en-US-ChristopherNeural" 
        
        async def _save():
            # Lowering pitch slightly (-5Hz) for a darker tone
            communicate = edge_tts.Communicate(text, voice, rate="+0%", pitch="-5Hz")
            await communicate.save(output_path)
            
        try:
            asyncio.run(_save())
            print(f"  [VOICE] Generated: {output_path}")
            return True
        except Exception as e:
            print(f"Error with Edge TTS: {e}")
            return False
