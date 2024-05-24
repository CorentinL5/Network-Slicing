import ipaddress
import tkinter as tk
from tkinter import ttk, messagebox

def calculate_network_info(previous_broadcast, group_size):
    new_mask = 32 - ((group_size+1).bit_length())
    adress_available = 2**(32 - new_mask)
    network = ipaddress.IPv4Network((previous_broadcast + 1, new_mask), strict=False)
    network_address = network.network_address
    broadcast_address = network.broadcast_address
    address_range = f"{network_address} - {broadcast_address}"

    return network_address, broadcast_address, address_range, adress_available, new_mask

def validate_inputs():
    try:
        base_network_ip = entry_base_network_ip.get()
        base_network_mask = int(entry_base_network_mask.get())
        list_of_groups = [int(x) for x in entry_list_of_groups.get().split(',')]

        # Validation des entrées
        ipaddress.IPv4Address(base_network_ip)
        if not (0 <= base_network_mask <= 32):
            raise ValueError("Le masque de sous-réseau doit être compris entre 0 et 32 inclus.")
        if not all(0 < group_size < 2**32 for group_size in list_of_groups):
            raise ValueError("Les tailles de groupe doivent être des nombres positifs.")

        return True
    except ValueError as e:
        messagebox.showerror("Erreur de saisie", str(e))
        return False

def display_results():
    if not validate_inputs():
        return

    base_network_ip = entry_base_network_ip.get()
    base_network_mask = int(entry_base_network_mask.get())
    list_of_groups = [int(x) for x in entry_list_of_groups.get().split(',')]

    previous_broadcast = ipaddress.IPv4Address(base_network_ip) - 1
    result_text.delete(1.0, tk.END)  # Clear previous results

    for group_size in list_of_groups:
        network_address, broadcast_address, address_range, address_available, subnet_mask = calculate_network_info(previous_broadcast, group_size)
        previous_broadcast = broadcast_address

        result_text.insert(tk.END, f"Pour le groupe de taille {group_size} :\n")
        result_text.insert(tk.END, f"Adresse réseau : {network_address}\n")
        result_text.insert(tk.END, f"Adresse de broadcast : {broadcast_address}\n")
        result_text.insert(tk.END, f"Plage d'adressage : {address_range}\n")
        result_text.insert(tk.END, f"Masque de sous-réseau : /{subnet_mask}\n")
        result_text.insert(tk.END, f"N° d'adresses, Théoriques : {address_available}, Disponibles : {address_available-2}\n\n")

# GUI setup
root = tk.Tk()
root.title("Calculateur de Sous-réseaux")

# Style
style = ttk.Style()
style.configure("TButton", padding=(10, 5), font='Helvetica 10 bold')

# Labels and Entry widgets
label_base_network_ip = ttk.Label(root, text="Adresse de réseau de base:")
entry_base_network_ip = ttk.Entry(root)
label_base_network_mask = ttk.Label(root, text="Masque de sous-réseau de base:")
entry_base_network_mask = ttk.Entry(root)
entry_base_network_mask.insert(tk.END, "/32")  # Default value
label_list_of_groups = ttk.Label(root, text="Liste des tailles de groupes (séparées par des virgules):")
entry_list_of_groups = ttk.Entry(root)
button_calculate = ttk.Button(root, text="Calculer", command=display_results)
result_text = tk.Text(root, height=15, width=60)

# Grid layout
label_base_network_ip.grid(row=0, column=0, sticky="w", padx=(10, 5), pady=(10, 5))
entry_base_network_ip.grid(row=0, column=1, padx=(5, 10), pady=(10, 5), sticky="ew")
label_base_network_mask.grid(row=1, column=0, sticky="w", padx=(10, 5), pady=5)
entry_base_network_mask.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="ew")
label_list_of_groups.grid(row=2, column=0, sticky="w", padx=(10, 5), pady=(5, 10))
entry_list_of_groups.grid(row=2, column=1, padx=(5, 10), pady=(5, 10), sticky="ew")
button_calculate.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="nsew")

# Configure grid resizing behavior
root.grid_rowconfigure(4, weight=1)  # Allow result_text to expand vertically
root.grid_columnconfigure(0, weight=1)  # Allow entry widgets and result_text to expand horizontally

# Center the GUI in the middle of the screen
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = int((screen_width - window_width) / 2)
y_position = int((screen_height - window_height) / 2)
root.geometry(f"+{x_position}+{y_position}")

# Start the GUI
root.mainloop()
