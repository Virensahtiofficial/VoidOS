import time
import random
import sys
import os
import zipfile
import requests

# Zorg ervoor dat de nodige modules geïnstalleerd zijn
os.system("pip install requests -q")

def clear():
    os.system('clear' if os.name != 'nt' else 'cls')  # Windows gebruikt 'cls', niet 'clear'

def loading_bar(label, length=30, speed=0.1):
    print(f"{label}", end="")
    for _ in range(length):
        print("-", end="", flush=True)
        time.sleep(speed)
    print(" DONE")

def download_file(url, destination):
    """Download een bestand van een URL naar de opgegeven bestemming."""
    response = requests.get(url)
    with open(destination, 'wb') as file:
        file.write(response.content)
    
def unzip_file(zip_file, destination):
    """Pak een ZIP-bestand uit naar een opgegeven map."""
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(destination)
    
def boot():
    clear()
    print("\033[92mBooting OS...\033[0m")
    time.sleep(3)
    
    loading_bar("Updating VoidOS...\n")
    # Stap 1: Download het ZIP-bestand naar /voidos
    url = "https://github.com/Virensahtiofficial/VoidOS/archive/refs/heads/main.zip"  # Vervang dit met je echte URL
    zip_path = "voidos/main.zip"
    download_file(url, zip_path)

    # Stap 2: Pak het ZIP-bestand uit naar de /voidos-map
    unzip_file(zip_path, "voidos")
    
    # Stap 3: Verplaats os.py naar de juiste locatie
    os.makedirs("voidos", exist_ok=True)  # Maak de map aan als die nog niet bestaat
    os.rename("voidos/VoidOS-main/os.py", "voidos/os.py")
    
    # Controleer of os.py nu correct is verplaatst
    if os.path.isfile("voidos/os.py"):
        print("\033[92mOS update successful!\033[0m")
    else:
        print("\033[91mError: os.py not found after update!\033[0m")
        sys.exit()

    time.sleep(2)
    os.system("python voidos/os.py")  # Start het OS script

if __name__ == "__main__":
    boot()