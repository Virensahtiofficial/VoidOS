import time
import random
import sys
import os
os.system("pip install bs4 requests -q")
def clear():
    os.system('clear' if os.name == 'nt' else 'clear')
def loading_bar(label, length=30, speed=0.1):
    print(f"{label}", end="")
    for _ in range(length):
        print("-", end="", flush=True)
        time.sleep(speed)
    print(" DONE")


def boot():
    clear()
    print("\033[92mBooting OS...\033[0m")
    time.sleep(3)
      
    loading_bar("Loading OS...\n")
    os.system("ls voidos")
    os.system("ls voidos/data")
    os.system("ls voidos/data/0")
    time.sleep(2)
    # Check if voidos/os.py exists
    if not os.path.isfile("voidos/os.py"):
        print("\033[91mError, OS files not found!\033[0m")
        time.sleep(3)
        clear()
        sys.exit()
    
    print("\n\033[92mVoidOS v1.0\033[0m")
    time.sleep(2)
    os.system("python voidos/os.py")

if __name__ == "__main__":
    boot()