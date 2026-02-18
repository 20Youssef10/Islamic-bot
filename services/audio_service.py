import requests
from pathlib import Path

AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)

def get_audio(ayah_id, reciter):
    file = AUDIO_DIR / f"{ayah_id}_{reciter}.mp3"
    if file.exists():
        return file

    url = f"https://api.alquran.cloud/v1/ayah/{ayah_id}/{reciter}"
    audio_url = requests.get(url).json()["data"]["audio"]
    file.write_bytes(requests.get(audio_url).content)
    return file