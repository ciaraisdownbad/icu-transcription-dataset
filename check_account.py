import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVEN_LABS_API_KEY"))

def check_status():
    print("🛰️ Connecting to ElevenLabs...")
    try:
        # 1. Check Character Balance
        user = client.user.get()
        remaining = user.subscription.character_count
        limit = user.subscription.character_limit
        print(f"📊 Credits: {remaining} / {limit} characters remaining.")

        # 2. List Available Voices
        print("\n🗣️ Your Available Voices:")
        voices = client.voices.get_all().voices
        for v in voices:
            print(f" - {v.name}: {v.voice_id} ({v.category})")
            
        if not voices:
            print("⚠️ No voices found! You might need to add some from the Library first.")
            
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    check_status()