import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import ctypes
import sys

# ---------------------------
# Élévation admin automatique
# ---------------------------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()

# ---------------------------
# Configuration des chemins
# ---------------------------
# ...existing code...
# ---------------------------
# Configuration des chemins
# ---------------------------
import glob

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Cherche l'exécutable NPI avec tolérance sur le nom
possible_npi = os.path.join(BASE_DIR, "nvidiaprofileinspector.exe")
if not os.path.exists(possible_npi):
    matches = glob.glob(os.path.join(BASE_DIR, "*profile*inspector*.exe"))
    possible_npi = matches[0] if matches else possible_npi

NPI_PATH = possible_npi
POTATO_PROFILE = os.path.join(BASE_DIR, "Fortnite_potato.nip")
DEFAULT_PROFILE = os.path.join(BASE_DIR, "Fortnite_default.nip")
# ...existing code...

# ---------------------------
# Fonction pour appliquer un profil
# ---------------------------
# ...existing code...
NPI_PATH = possible_npi
POTATO_PROFILE = os.path.join(BASE_DIR, "Fortnite_potato.nip")
DEFAULT_PROFILE = os.path.join(BASE_DIR, "Fortnite_default.nip")
# ...existing code...

# --- Diagnostic simple pour aider à localiser nvidiaprofileinspector.exe ---
def _debug_list_dir():
    try:
        files = os.listdir(BASE_DIR)
    except Exception as e:
        files = [f"Erreur lecture dossier: {e}"]
    return files

print("DEBUG: BASE_DIR =", BASE_DIR)
print("DEBUG: NPI_PATH =", NPI_PATH)
print("DEBUG: fichiers dans BASE_DIR =", _debug_list_dir())

# ---------------------------
# Fonction pour appliquer un profil
# ---------------------------
def apply_profile(profile_path):
    if not os.path.exists(NPI_PATH):
        files = _debug_list_dir()
        msg = (
            "NVIDIA Profile Inspector introuvable.\n\n"
            f"Chemin cherché : {NPI_PATH}\n\n"
            "Fichiers trouvés dans le dossier :\n" + "\n".join(files)
        )
        # affiche boîte d'erreur et log dans la console
        messagebox.showerror("Erreur", msg)
        print("ERROR:", msg)
        return
    if not os.path.exists(profile_path):
        messagebox.showerror("Erreur", f"Profil introuvable : {os.path.basename(profile_path)}")
        return
    try:
        subprocess.run([NPI_PATH, "-import", profile_path], check=True)
        messagebox.showinfo("Succès", f"Profil appliqué : {os.path.basename(profile_path)}")
    except subprocess.CalledProcessError:
        messagebox.showerror("Erreur", "Impossible d'appliquer le profil.")
    except Exception as e:
        messagebox.showerror("Erreur inattendue", str(e))
# ...existing code...

# ---------------------------
# Interface graphique
# ---------------------------
root = tk.Tk()
root.title("🥔 Potato Tool")
root.geometry("350x200")
root.resizable(False, False)

label = tk.Label(root, text="Fortnite Potato Tool", font=("Arial", 16, "bold"))
label.pack(pady=15)

start_button = tk.Button(root, text="Start Potato Graphics 🥔", font=("Arial", 12),
                         bg="#2ecc71", fg="white", width=30,
                         command=lambda: apply_profile(POTATO_PROFILE))
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Deactivate Potato Graphics 🌈", font=("Arial", 12),
                        bg="#e74c3c", fg="white", width=30,
                        command=lambda: apply_profile(DEFAULT_PROFILE))
stop_button.pack(pady=10)

root.mainloop()
