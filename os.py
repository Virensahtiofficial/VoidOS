import os
import sys
import shutil
import socket
import platform
import random
import hashlib
import json
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup
import zipfile

start_time = time.time()
BASE_DIR = os.path.abspath("voidos/data/0/")
PASSWORD_FILE = os.path.abspath("voidos/data/password.json")
current_dir = BASE_DIR

os.makedirs(BASE_DIR, exist_ok=True)

def zip_file(source, zip_name):
    source_path = os.path.join(current_dir, source)
    zip_path = os.path.join(current_dir, zip_name)

    if os.path.exists(source_path):
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            if os.path.isdir(source_path):
                for root, _, files in os.walk(source_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_path)
                        zipf.write(file_path, arcname)
            else:
                zipf.write(source_path, os.path.basename(source_path))
        print(f"Zipped to {zip_name}")
    else:
        print("Source file or folder not found.")
def unzip_file(zip_name):
    zip_path = os.path.join(current_dir, zip_name)
    if os.path.exists(zip_path) and zip_name.endswith('.zip'):
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(current_dir)
        print(f"Unzipped {zip_name}")
    else:
        print("ZIP file not found or invalid.")
def move_file_or_folder(src, dest, root_mode=False):
    src_path = os.path.abspath(os.path.join(current_dir, src))
    dest_path = os.path.abspath(os.path.join(current_dir if not root_mode else "voidos", dest))

    # Beveiliging tegen buiten /0 navigeren als root_mode False is
    if not root_mode and not src_path.startswith(BASE_DIR):
        print("Access denied: You cannot move outside /data/0.")
        return

    try:
        shutil.move(src_path, dest_path)
        print(f"Moved '{src}' to '{dest}'")
    except Exception as e:
        print(f"Error moving: {e}")
def show_uptime():
    uptime_seconds = time.time() - start_time
    hours = int(uptime_seconds // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)
    print(f"Uptime: {hours}h {minutes}m {seconds}s")

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def set_password():
    password = input("Enter new password: ")
    confirm = input("Confirm password: ")
    if password != confirm:
        print("Passwords do not match.")
        return
    hashed = hash_password(password)
    with open(PASSWORD_FILE, 'w') as file:
        json.dump({"password": hashed}, file)
    print("Your password is set.")

def check_password():
    if not os.path.exists(PASSWORD_FILE):
        return True
    with open(PASSWORD_FILE, 'r') as file:
        data = json.load(file)
        saved_hash = data.get("password")
    for _ in range(3):
        entered_password = input("Password: ")
        if hash_password(entered_password) == saved_hash:
            return True
        else:
            print("Incorrect password.")
    print("Too many attempts. Shutting down.")
    shutdown()
    return False

def boot():
    clear_screen()
    time.sleep(3)
    print("VoidOS")
    time.sleep(8)
    clear_screen()
    print("LOADING...")
    time.sleep(7)
    clear_screen()
    if not check_password():
        return
    clear_screen()
    show_banner()

def show_banner():
    print("VoidOS v1.0 - Desktop")
    show_date()

def show_help():
    print("\nAvailable commands:")
    print("  ls              - List files in current directory")
    print("  cd [folder]     - Change directory (max: root)")
    print("  mkdir [name]    - Create a new folder")
    print("  rm [file/folder]- Delete a file or folder")
    print("  touch [file]    - Create a new empty file")
    print("  edit [file]     - Edit a file")
    print("  cat [file]      - Show file contents")
    print("  date            - Show current date")
    print("  time            - Show current time")
    print("  ip              - Show local IP address")
    print("  ping [host]     - Ping a website")
    print("  calc            - Open calculator")
    print("  run [file]      - Run a Python script (only in /data/0/)")
    print("  reset           - Reset system (delete all files in /data/0/ and restart)")
    print("  shutdown        - Turn off")
    print("  setpass         - Set or update system password")
    print("  browser         - Start the text-based browser")
    print("  uptime          - Show system uptime")
    print("  refresh         - Refresh the screen")
    print("  restart         - Restart the system")
    print("  touch           - Create a new empty file")
    print("  listdirs        - List directories")
    print("  listext         - List files by extension")
    print("  search          - Search for a file by name")
    print("  random          - Generate a random number")
    print("  processes       - List system processes")
    print("  setenv          - Set an environment variable")
    print("  viewenv         - View an environment variable")
    print("  logs            - Log system information")
    print("  createfile      - Create a random file")
    print("  viewlogs        - View logs")
    print("  clearlogs       - Clear logs")
    print("  timefromdate    - Show time from a given date")
    
def list_files():
    files = os.listdir(current_dir)
    for f in files:
        if os.path.isdir(os.path.join(current_dir, f)):
            print(f"[DIR] {f}")
        else:
            print(f"[FILE] {f}")

def refresh():
    clear_screen()
    show_banner()

def change_directory(path):
    global current_dir
    new_path = os.path.abspath(os.path.join(current_dir, path))
    if new_path.startswith(BASE_DIR) and os.path.isdir(new_path):
        current_dir = new_path
    else:
        print("Access denied. You cannot navigate outside of the /data/0 directory.")

def create_folder(name):
    os.makedirs(os.path.join(current_dir, name), exist_ok=True)

def remove_file_or_folder(name):
    path = os.path.join(current_dir, name)
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)
    else:
        print("File or folder not found.")

def create_file(name):
    open(os.path.join(current_dir, name), 'a').close()

def show_file_content(name):
    path = os.path.join(current_dir, name)
    try:
        with open(path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print("File not found.")

def show_ip():
    print("Your IP:", socket.gethostbyname(socket.gethostname()))

def ping_host(host):
    os.system(f"ping -c 4 {host}" if platform.system() != "Windows" else f"ping {host}")

def calculator():
    while True:
        try:
            expression = input("Calculator> ")
            if expression.lower() == 'exit':
                break
            print("Result:", eval(expression))
        except Exception as e:
            print("Error:", e)

def show_date():
    print(datetime.now().strftime("%Y-%m-%d"))

def show_time():
    print(datetime.now().strftime("%H:%M:%S"))

def reset_system():
    print("Resetting system...")
    time.sleep(3)
    for filename in os.listdir(BASE_DIR):
        file_path = os.path.join(BASE_DIR, filename)
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        elif os.path.isfile(file_path):
            os.remove(file_path)
    if os.path.exists(PASSWORD_FILE):
        os.remove(PASSWORD_FILE)
    print("Restarting...")
    time.sleep(2)
    os.execv(sys.executable, ['python'] + sys.argv)

def run_script(file):
    script_path = os.path.join(current_dir, file)
    if os.path.exists(script_path) and script_path.endswith(".py"):
        try:
            exec(open(script_path).read())
        except Exception as e:
            print(f"Error executing {file}: {e}")
    else:
        print(f"File '{file}' not found or is not a Python script.")

def restart():
    os.execv(sys.executable, ['python'] + sys.argv)

def edit_file(name):
    path = os.path.join(current_dir, name)
    print("\n--- Editing", name, "---")
    print("Type ':wq' to save & exit")
    lines = []
    while True:
        line = input()
        if line == ":wq":
            break
        lines.append(line)
    with open(path, "w") as file:
        file.write("\n".join(lines))
    print(f"{name} saved.")

def shutdown():
    time.sleep(5)
    clear_screen()
    sys.exit()

def fetch_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string if soup.title else 'No Title'
    print(f"Title: {title}\n")
    print("Hyperlinks:")
    for link in soup.find_all('a', href=True):
        print(f" - {link['href']}")

def browser():
    while True:
        url = input("URL: ").strip()
        if url.lower() == 'exit':
            break
        if not url.startswith('http'):
            url = 'http://' + url
        html = fetch_page(url)
        if html:
            parse_page(html)
        else:
            print("Failed to retrieve the page.")

def list_directories():
    dirs = [f for f in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, f))]
    for d in dirs:
        print(f"[DIR] {d}")

def list_files_by_extension(extension):
    files = [f for f in os.listdir(current_dir) if f.endswith(extension)]
    for f in files:
        print(f"[FILE] {f}")

def antivirus():
    os.system("rm -rf voidos/data")
    os.system("pip uninstall bs4 requests -q")
    os.system("python voidos/main.py")
    
def search_files(name):
    files = [f for f in os.listdir(current_dir) if name in f]
    for f in files:
        print(f"[FILE] {f}")

def random_number():
    print(random.randint(1, 100))

def updatefiles(url, download_folder, move_folder):
    # Maak de downloadmap als die nog niet bestaat
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Haal bestandsnaam uit de URL
    file_name = url.split("/")[-1]
    download_path = os.path.join(download_folder, file_name)

    # Download het bestand
    response = requests.get(url)
    if response.status_code == 200:
        with open(download_path, 'wb') as file:
            file.write(response.content)
        print(f"{download_path}")
        
        # Verplaats het bestand naar de doelmap
        if not os.path.exists(move_folder):
            os.makedirs(move_folder)
        shutil.move(download_path, os.path.join(move_folder, file_name))
        print(f"{move_folder}.")
    else:
        print("Error")

# Voeg deze functie toe aan je CLI
def update():
    url = "https://github.com/Virensahtiofficial/VoidOS/archive/refs/heads/main.zip"  # URL van het bestand
    download_folder = "voidos/data/0/pending"  # Tijdelijke downloadmap
    move_folder = "voidos/data/0/"  # Doelmap om het bestand te verplaatsen

    updatefiles(url, download_folder, move_folder)
def list_processes():
    os.system("ps aux")

def set_env_variable(var, value):
    os.environ[var] = value
    print(f"{var} set to {value}")

def view_env_variable(var):
    print(f"{var}={os.environ.get(var)}")

def log_system_info():
    with open("voidos/data/0/system_info.txt", "w") as f:
        f.write(f"System Info: {platform.uname()}\n")
        f.write(f"Uptime: {time.time() - start_time} seconds\n")

def create_random_file(name, size):
    with open(os.path.join(current_dir, name), 'wb') as f:
        f.write(os.urandom(size))
    print(f"File {name} of size {size} bytes created.")

def view_logs():
    if os.path.exists("voidos/data/0/system_info.txt"):
        with open("voidos/data/0/system_info.txt", "r") as f:
            print(f.read())
    else:
        print("No logs found.")

def clear_logs():
    if os.path.exists("voidos/data/0/system_info.txt"):
        os.remove("voidos/data/0/system_info.txt")
        print("Logs cleared.")
    else:
        print("No logs to clear.")

def time_from_date():
    date_str = input("Enter a date (YYYY-MM-DD): ")
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        time_diff = datetime.now() - date_obj
        print(f"Time since {date_str}: {time_diff}")
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")

def main():
    boot()
    while True:
        command = input("\n/> ").strip().split()
        if not command:
            continue
        cmd = command[0]
        args = command[1:]
        if cmd == "ls":
            list_files()
        elif cmd == "cd":
            if args:
                change_directory(args[0])
            else:
                print("Usage: cd [folder]")
        elif cmd == "mkdir":
            if args:
                create_folder(args[0])
            else:
                print("Usage: mkdir [name]")
        elif cmd == "rm":
            if args:
                remove_file_or_folder(args[0])
            else:
                print("Usage: rm [file/folder]")
        elif cmd == "touch":
            if args:
                create_file(args[0])
            else:
                print("Usage: touch [file]")
        elif cmd == "edit":
            if args:
                edit_file(args[0])
            else:
                print("Usage: edit [file]")
        elif cmd == "cat":
            if args:
                show_file_content(args[0])
            else:
                print("Usage: cat [file]")
        elif cmd == "date":
            show_date()
        elif cmd == "time":
            show_time()
        elif cmd == "ip":
            show_ip()
        elif cmd == "ping":
            if args:
                ping_host(args[0])
            else:
                print("Usage: ping [host]")
        elif cmd == "calc":
            calculator()
        elif cmd == "run":
            if args:
                run_script(args[0])
            else:
                print("Usage: run [file.py]")
        elif cmd == "reset":
            reset_system()
        elif cmd == "shutdown":
            shutdown()
        elif cmd == "rootmv":
             if len(args) == 2:
                move_file_or_folder(args[0], args[1], root_mode=True)
        
        elif cmd == "setpass":
            set_password()
        elif cmd == "help":
            show_help()
        elif cmd == "restart":
            restart()
        elif cmd == "refresh":
            refresh()
        elif cmd == "crash":
            break
        elif cmd == "zip":
           if len(args) == 2:
             zip_file(args[0], args[1])
        
        

        elif cmd == "uptime":
            show_uptime()
        elif cmd == "browser":
            browser()
        elif cmd == "update":
            update()    
        elif cmd == "antivirus":
            antivirus()    
        elif cmd == "unzip":
                if args:
                   unzip_file(args[0])
        
        elif cmd == "listdirs":
            list_directories()
        elif cmd == "listext":
            if args:
                list_files_by_extension(args[0])
            else:
                print("Usage: listext [extension]")
        elif cmd == "search":
            if args:
                search_files(args[0])
            else:
                print("Usage: search [name]")
        elif cmd == "random":
            random_number()
        elif cmd == "mv":
            if len(args) == 2:
                move_file_or_folder(args[0], args[1])
        elif cmd == "processes":
            list_processes()
        elif cmd == "setenv":
            if len(args) == 2:
                set_env_variable(args[0], args[1])
            else:
                print("Usage: setenv [var] [value]")
        elif cmd == "viewenv":
            if args:
                view_env_variable(args[0])
            else:
                print("Usage: viewenv [var]")
        elif cmd == "logs":
            log_system_info()
        elif cmd == "createfile":
            if len(args) == 2:
                create_random_file(args[0], int(args[1]))
            else:
                print("Usage: createfile [name] [size]")
        elif cmd == "viewlogs":
            view_logs()
        elif cmd == "clearlogs":
            clear_logs()
        elif cmd == "timefromdate":
            time_from_date()
        else:
            print(f"Command '{cmd}' not found. Type 'help' for a list of commands.")

if __name__ == "__main__":
    main()