import json
import os

from scripts.api_client import APIClient

class PsychologyResearcher:
    def __init__(self, topic, length_minutes=5):
        self.topic = topic
        self.length_minutes = length_minutes
        self.client = APIClient()
        
    def generate_manifest(self):
        prompt = self.generate_system_prompt()
        print(f"Sending prompt to Grok for topic: {self.topic}...")
        manifest_data = self.client.call_grok(prompt)
        
        if manifest_data:
            path = self.save_manifest(manifest_data)
            print(f"Manifest saved to {path}")
            return path
        else:
            print("Failed to generate manifest from Grok.")
            return None
        
    def generate_system_prompt(self):
        return f"""
        You are the Head Scriptwriter for 'PSYCHO STUDIO AI', a viral YouTube channel specializing in Dark Psychology and Human Behavior.
        Your target audience is Gen Z. Your style is edgy, fast-paced, and highly manipulative (in a cinematic way).
        
        TASK:
        Generate a full production manifest for a {self.length_minutes}-minute video on the topic: '{self.topic}'.
        
        STRUCTURE:
        1. THE HOOK (0:00-0:30): Must be a "Pattern Interrupt". Start with a shocking statement or a question that triggers 'FOMO' or 'Fear'.
        2. THE REVEAL: Introduce the psychological concept.
        3. THE 'TRICK': Give a practical (or dark) application of the concept.
        4. THE CLIFFHANGER: Transition to the next sub-topic.
        
        OUTPUT FORMAT:
        You must output ONLY a valid JSON object. No intro text.
        
        JSON SCHEMA:
        {{
            "metadata": {{
                "title": "...",
                "vibe": "Moody/Dark/Cinematic",
                "color_palette": ["#000000", "#FF0000", "#FFFFFF"]
            }},
            "scenes": [
                {{
                    "scene_id": 1,
                    "duration_estimate": 8,
                    "narration": "The words the voiceover will speak.",
                    "on_screen_text": ["TEXT 1", "TEXT 2"],
                    "visual_queries": ["specific stock footage search term 1", "term 2"],
                    "sfx_cue": "whoosh / heartbeat / glitch",
                    "music_mood": "dark_ambient",
                    "transition": "glitch_fade"
                }}
            ]
        }}
        
        CRITICAL RULES FOR VISUALS:
        - NEVER use literal searches. (e.g., Don't use 'money' for wealth).
        - USE METAPHORS:
            * Manipulation -> "Puppet strings", "Chess piece moving", "Invisible ink".
            * Secrets/Darkness -> "Keyhole view", "Shadow moving behind curtain", "Deep water".
            * Human Mind -> "Labyrinth", "Clockwork gears", "Electric neurons".
            * Social Pressure -> "Crushing trash compactor", "Fish swimming against current".
        - Every scene must have at least 2 visual queries to allow the editor to cut between them.
        """

    def save_manifest(self, data):
        path = f"psycho_studio/outputs/manifest_{self.topic.replace(' ', '_').lower()}.json"
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
        return path

# Example Usage logic (Placeholder for actual API call)
if __name__ == "__main__":
    # This is where we would call Grok/LLM
    print("Researcher initialized for topic: " + "The Art of Social Manipulation")
