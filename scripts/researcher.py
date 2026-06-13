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
        Your response must be a 10-15 minute deep dive, broken into 5 clear ACTS:
        ACT 1: THE HOOK (0:00-2:00) - Intense pacing, fast cuts, high mystery.
        ACT 2: THE ANATOMY (2:00-5:00) - Scientific explanation, slower pace, data graphics.
        ACT 3: THE DARK TRUTH (5:00-8:00) - The most shocking part. Metaphorical visuals.
        ACT 4: REAL WORLD EXAMPLES (8:00-12:00) - Case studies or 'how to spot it'.
        ACT 5: THE DEFENSE/OUTRO (12:00-15:00) - Empowerment and a cliffhanger for the next video.

        CRITICAL RULES FOR LONG FORM:
        - Every 2 minutes, create a 'Pattern Interrupt' (a sudden change in music mood or a shocking visual).
        - Use 'Cliffhangers' at the end of every Act.
        
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
