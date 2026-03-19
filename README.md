#  ICU Transcription Dataset Generator

This project automates the creation of high-fidelity, "messy" medical dialogue for training and testing clinical transcription models. It simulates the high-stress environment of an Intensive Care Unit (ICU) by layering professional medical speech with realistic environmental noise.

##  Project Structure
* **`generate_pilot.py`**: The main engine. Uses **Claude 4.6** to write scripts and **ElevenLabs Flash 2.5** to synthesize voices.
* **`mix_icu_audio.py`**: An audio processing tool that layers background ICU noises (ventilators, alarms) over clean dialogue using `pydub`.
* **`check_account.py`**: A diagnostic script to verify ElevenLabs API permissions and available Voice IDs.
* **`outputs/`**: Storage for generated `.mp3` files (e.g., `icu_technical_chaos.mp3`).

##  Getting Started

### 1. Prerequisites
Ensure you have Python 3.14+ installed.

### 2. Environment Setup
```bash
# Initialize and activate the virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required libraries
pip install anthropic elevenlabs pydantic python-dotenv pydub
```

### 3. Configuration
Create a `.env` file in the root directory and add your API credentials:
```env
ANTHROPIC_API_KEY=your_key_here
ELEVEN_LABS_API_KEY=your_key_here
```

##  How to Run
1.  **Generate Clean Dialogue**: Run `python3 generate_pilot.py`. This creates a 60-second script with complex terms like *Dexmedetomidine*.
2.  **Add Realism**: Ensure an ambient noise file exists in `data/icu_ambience.mp3`, then run `python3 mix_icu_audio.py` to create the final "Production" mix.

---
