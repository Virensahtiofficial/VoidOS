import requests
import os

# URL van het bestand
url = "https://raw.githubusercontent.com/Virensahtiofficial/VoidOS/016efe974b7e718af9a274b140a5e0e002cddd56/os.py"  # Vervang dit met jouw URL

# Specifieke map instellen
doelmap = "voidos"  # Verander dit naar jouw gewenste map
bestand_naam = "os.py"  # Naam van het opgeslagen bestand

# Controleer of de map bestaat, anders maak hem aan
if not os.path.exists(doelmap):
    os.makedirs(doelmap)

# Volledig pad naar het bestand
bestand_pad = os.path.join(doelmap, bestand_naam)

try:
    print("Updating system...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(bestand_pad, "wb") as bestand:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                bestand.write(chunk)

    print("Updated successfully!")
    os.system("python voidos/os.py")
except requests.RequestException as e:
    print(f"{e}")
