import time
import random
import sys
import os
os.system("pip install requests bs4 -q")
import zipfile
import requests

# Zorg ervoor dat de nodige modules geïnstalleerd zijn

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
    try:
        response = requests.get(url)
        response.raise_for_status()  # Gooi een exception bij een slechte statuscode
        with open(destination, 'wb') as file:
            file.write(response.content)
        print(f"{destination}")
    except requests.exceptions.RequestException as e:
        print(f"{e}")
        return False  # Geef aan dat het downloaden niet gelukt is
    return True

def unzip_file(zip_file, destination):
    """Pak een ZIP-bestand uit naar een opgegeven map."""
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(destination)
        print(f"{zip_file} {destination}")
    except zipfile.BadZipFile as e:
        print(f"{e}")
        return False  # Geef aan dat het uitpakken niet gelukt is
    except FileNotFoundError:
        print(f"Not found: {zip_file}")
        return False
    return True

def boot():
    clear()
    print("\033[92mBooting OS...\033[0m")
    time.sleep(3)
    
    loading_bar("Updating VoidOS...\n")
    
    # Stap 1: Download het ZIP-bestand naar /voidos
    url = "https://github.com/Virensahtiofficial/VoidOS/archive/refs/heads/main.zip"  # Vervang dit met je echte URL
    zip_path = "voidos/main.zip"
    
    # Als het downloaden mislukt, ga dan verder met het opstarten van het OS
    if not download_file(url, zip_path):
        print("\033[93mSkipping update due to download error...\033[0m")
    
    # Stap 2: Pak het ZIP-bestand uit naar de /voidos-map (alleen als het bestand gedownload is)
    if os.path.isfile(zip_path) and unzip_file(zip_path, "voidos"):
        # Stap 3: Verplaats os.py naar de juiste locatie
        os.makedirs("voidos", exist_ok=True)  # Maak de map aan als die nog niet bestaat
        try:
            os.rename("voidos/VoidOS-main/os.py", "voidos/os.py")
            os.rename("voidos/VoidOS-main/updater.py", "voidos/updater.py")
        except FileNotFoundError as e:
            print(f"{e}")
        
        # Controleer of os.py nu correct is verplaatst
        if os.path.isfile("voidos/os.py"):
            os.system("rm -rf voidos/VoidOS-main")
            os.system("rm -rf voidos/main.zip")
            os.system("ls voidos")
            os.system("ls voidos/data")
            os.system("ls voidos/data/0")
            print("\033[92mOS update successful!\033[0m")
        else:
            print("\033[91mError: os.py not found after update!\033[0m")
    else:
        print("\033[93mUpdate failed, starting current version...\033[0m")
    
    # Start het OS script (zelfs als er geen update is)
    time.sleep(2)
    os.system("python voidos/os.py")  # Start het OS script

if __name__ == "__main__":
    boot()
