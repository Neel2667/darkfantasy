import requests
import json
import os

class EachLabsClient:
    def __init__(self, config_path="psycho_studio/config.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        self.api_key = self.config['api_keys'].get('eachlabs')
        self.base_url = "https://eachsense-agent.core.eachlabs.run/v1/chat/completions"

    def edit_video(self, video_url, prompt):
        """
        Sends a video to each::sense for AI-powered editing.
        """
        if not self.api_key or "YOUR" in self.api_key:
            print("❌ EachLabs API Key missing. Skipping AI Edit.")
            return None

        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
        
        data = {
            "messages": [
                {
                    "role": "user", 
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": video_url}}
                    ]
                }
            ],
            "stream": False
        }

        print(f"✨ AI EDITING START: {prompt[:50]}...")
        try:
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            # The API returns the URL of the edited video in the content
            result = response.json()
            edited_video_url = result['choices'][0]['message']['content']
            return edited_video_url
        except Exception as e:
            print(f"❌ EachLabs API Error: {e}")
            return None
