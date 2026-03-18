from pydub import AudioSegment
import os

def mix_clinical_audio(voice_file, background_noise_file):
    # 1. Load the files
    voice = AudioSegment.from_file(voice_file)
    background = AudioSegment.from_file(background_noise_file)

    # 2. Lower the background volume so it doesn't drown out the doctors
    # -25dB to -30dB is usually the "Sweet Spot" for realism
    background = background - 25 

    # 3. Loop the background if it's shorter than the dialogue
    if len(background) < len(voice):
        background = background * (len(voice) // len(background) + 1)
    
    background = background[:len(voice)]

    # 4. Overlay the voice onto the background
    combined = background.overlay(voice)

    # 5. Export
    output_path = "outputs/icu_final_production.mp3"
    combined.export(output_path, format="mp3")
    print(f"✅ Final Production mixed: {output_path}")

if __name__ == "__main__":
    # You can download a 10-second 'ICU Ambient' clip from YouTube/Freesound
    # and save it as 'data/icu_ambience.mp3'
    mix_clinical_audio("outputs/icu_pilot_raw.mp3", "data/icu_ambience.mp3")