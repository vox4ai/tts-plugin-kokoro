import urllib.request
from pathlib import Path
try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

# Configuration: Representative Kokoro-82M model and voices
MODELS_DIR = Path("models")
FILES_TO_DOWNLOAD = {
    "kokoro-v1_0.pth": "https://huggingface.co/hexgrad/Kokoro-82M/resolve/main/kokoro-v1_0.pth",
}

def download_file(url: str, dest: Path):
    if dest.exists():
        print(f"File already exists: {dest}")
        return

    print(f"Downloading {url} to {dest}...")
    try:
        with urllib.request.urlopen(url) as response:
            file_size = int(response.getheader('Content-Length', 0))
            
            if tqdm:
                with tqdm(total=file_size, unit='B', unit_scale=True, desc=dest.name) as pbar:
                    with open(dest, 'wb') as out_file:
                        while True:
                            chunk = response.read(8192)
                            if not chunk:
                                break
                            out_file.write(chunk)
                            pbar.update(len(chunk))
            else:
                with open(dest, 'wb') as out_file:
                    out_file.write(response.read())
        print(f"Successfully downloaded {dest.name}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        raise

def main():
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Initializing Kokoro-TTS models in {MODELS_DIR.absolute()}...")
    
    for filename, url in FILES_TO_DOWNLOAD.items():
        dest_path = MODELS_DIR / filename
        download_file(url, dest_path)

    print("\nAll models downloaded successfully.")

if __name__ == "__main__":
    main()
