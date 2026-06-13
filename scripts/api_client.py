import requests
import json
import os

class APIClient:
    def __init__(self, config_path="psycho_studio/config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.keys = self.config['api_keys']

    def call_grok(self, prompt):
        """Calls the Grok/X.AI API (or compatible OpenAI-style endpoint)"""
        url = "https://api.x.ai/v1/chat/completions" # Placeholder for Grok API URL
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.keys['grok']}"
        }
        data = {
            "model": "grok-beta", # Replace with current Grok model name
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
            # Find the JSON block in case there's preamble
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            return json.loads(content)
        except Exception as e:
            print(f"Error calling Grok: {e}")
            return None

    def download_pexels_video(self, query, output_path):
        """Searches and downloads the best vertical/horizontal clip from Pexels"""
        url = "https://api.pexels.com/videos/search"
        headers = {"Authorization": self.keys['pexels']}
        params = {
            "query": query,
            "per_page": 1,
            "orientation": "landscape"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            if data['videos']:
                # Get the link for a HD file
                video_files = data['videos'][0]['video_files']
                # Prefer HD (1920x1080)
                link = next((f['link'] for f in video_files if f['width'] == 1920), video_files[0]['link'])
                
                # Download the file
                vid_data = requests.get(link).content
                with open(output_path, 'wb') as f:
                    f.write(vid_data)
                return True
        except Exception as e:
            print(f"Error downloading Pexels video for '{query}': {e}")
        return False

    def generate_elevenlabs_voice(self, text, output_path):
        """Generates voiceover using ElevenLabs"""
        voice_id = "pNInz6obpgnuMvscL7PR" # Example 'Josh' voice ID
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.keys['elevenlabs']
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return True
        except Exception as e:
            print(f"Error calling ElevenLabs: {e}")
        return False
