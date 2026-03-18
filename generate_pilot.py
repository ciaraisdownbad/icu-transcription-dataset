import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from elevenlabs.client import ElevenLabs
from pydantic import BaseModel

# 1. SETUP
load_dotenv()
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
eleven_client = ElevenLabs(api_key=os.getenv("ELEVEN_LABS_API_KEY"))

# 2. YOUR VERIFIED VOICE MAP
VOICE_MAP = {
    "Dr. Hanley": "pNInz6obpgDQGcFmaJgB",      # Adam (Dominant/Firm)
    "Dr. Dheeraj": "XrExE9yKIg1WjnnlVkGX",     # Matilda (Professional)
    "Dr. Rossi": "N2lVS1w4EtoT3dr4eOWO",       # Callum (Husky/Muttery)
    "Nurse Sarah": "hpp4J3VqNfWAUOO0d1Us",     # Bella (Professional/Bright)
    "Resident Mike": "CwhRBWXzGAHq8TQ4Fs17",   # Roger (Laid-back/Casual)
    "Dr. Chen": "Xb7hH8MSUJpSbSDYk0k2"         # Alice (Clear/Engaging)
}

class DialogueLine(BaseModel):
    speaker: str
    text: str

class ICUScript(BaseModel):
    dialogue: list[DialogueLine]

def run_pilot():
    print("🧠 Step 1: Claude is writing a 'Messy' Technical Script...")
    
    # We explicitly tell Claude to include stutters and jargon
    prompt = """Write a 45-second ICU dialogue between Dr. Hanley and Dr. Rossi. 
    They are arguing about a failing ventilator and potential exsanguination. 
    Use complex terms: 'Dexmedetomidine', 'Pneumothorax', and 'Norepinephrine'.
    
    CRITICAL INSTRUCTIONS: 
    1. Write like real, panicked speech. 
    2. Use 'um', 'uh', and repeat words (e.g., 'The-the-the blood pressure'). 
    3. Use phonetic stutters like 'D-D-Dex' and 'P-P-Pneumo'.
    4. Make the sentences break off mid-thought."""

    response = anthropic_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        tools=[{
            "name": "record_script",
            "description": "Record ICU dialogue",
            "input_schema": ICUScript.model_json_schema()
        }],
        tool_choice={"type": "tool", "name": "record_script"},
        messages=[{"role": "user", "content": prompt}]
    )

    script_data = response.content[0].input['dialogue']
    
    print(f"🎙️ Step 2: ElevenLabs generating with Stability=0.15 (Chaos Mode)...")
    final_audio = b"" 

    for line in script_data:
        speaker = line.get('speaker', 'Dr. Hanley')
        voice_id = VOICE_MAP.get(speaker, VOICE_MAP["Dr. Hanley"])
        
        print(f"  -> Generating {speaker}...")
        
        try:
            audio_gen = eleven_client.text_to_speech.convert(
                voice_id=voice_id,
                text=line['text'],
                model_id="eleven_flash_v2_5", 
                voice_settings={
                    "stability": 0.15,      # Forces vocal cracks and speed changes
                    "similarity_boost": 0.8,
                    "style": 0.45           # Adds more personality/accent
                }
            )
            for chunk in audio_gen:
                final_audio += chunk
        except Exception as e:
            print(f"⚠️ Error on {speaker}: {e}")

    # 4. SAVE
    os.makedirs("outputs", exist_ok=True)
    file_path = "outputs/icu_technical_chaos.mp3"
    with open(file_path, "wb") as f:
        f.write(final_audio)
    
    print(f"\n✅ DONE! Listen to '{file_path}'")

if __name__ == "__main__":
    run_pilot()