import tkinter as tk
from tkinter import ttk
import os
import re

# Path to the folder containing the Pokémon data files
folder_path = r"D:\PokemonCrystal-main\PokemonCrystal-main\data\pokemon\base_stats"

# Regular expressions to extract relevant data from the file
base_stat_pattern = re.compile(r"db\s+(\d+),\s+(\d+),\s+(\d+),\s+(\d+),\s+(\d+),\s+(\d+)\s*;\s*hp\s*atk\s*def\s*spd\s*sat\s*sdf", re.IGNORECASE)
type_pattern = re.compile(r"db\s+(\w+),\s*(\w+)\s*;\s*type", re.IGNORECASE)
catch_rate_pattern = re.compile(r"db\s+(\d+)\s*;\s*catch rate", re.IGNORECASE)
base_exp_pattern = re.compile(r"db\s+(\d+)\s*;\s*base exp", re.IGNORECASE)
gender_ratio_pattern = re.compile(r"db\s+(\w+)\s*;\s*gender ratio", re.IGNORECASE)

# Function to load a Pokémon's data
def load_pokemon_data(pokemon_name):
    file_path = os.path.join(folder_path, f"{pokemon_name}.asm")
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract the base stats, type, catch rate, base exp, and gender ratio
    base_stat_match = base_stat_pattern.search(content)
    type_match = type_pattern.search(content)
    catch_rate_match = catch_rate_pattern.search(content)
    base_exp_match = base_exp_pattern.search(content)
    gender_ratio_match = gender_ratio_pattern.search(content)

    if base_stat_match:
        hp.set(base_stat_match.group(1))
        attack.set(base_stat_match.group(2))
        defense.set(base_stat_match.group(3))
        speed.set(base_stat_match.group(4))
        special_attack.set(base_stat_match.group(5))
        special_defense.set(base_stat_match.group(6))

    if type_match:
        primary_type.set(type_match.group(1))
        secondary_type.set(type_match.group(2))

    if catch_rate_match:
        catch_rate.set(catch_rate_match.group(1))

    if base_exp_match:
        base_exp.set(base_exp_match.group(1))

    if gender_ratio_match:
        gender_ratio.set(gender_ratio_match.group(1))

# Function to save the modified data back to the file
def save_pokemon_data():
    pokemon_name = pokemon_dropdown.get()
    file_path = os.path.join(folder_path, f"{pokemon_name}.asm")

    with open(file_path, 'r') as file:
        content = file.read()

    # Replace the base stats
    new_base_stats = f"db  {hp.get()},  {attack.get()},  {defense.get()},  {speed.get()},  {special_attack.get()},  {special_defense.get()} \n    ;   hp  atk  def  spd  sat  sdf"
    content = re.sub(base_stat_pattern, new_base_stats, content)

    # Replace the types
    new_types = f"db {primary_type.get()}, {secondary_type.get()} ; type"
    content = re.sub(type_pattern, new_types, content)

    # Replace the catch rate
    new_catch_rate = f"db {catch_rate.get()} ; catch rate"
    content = re.sub(catch_rate_pattern, new_catch_rate, content)

    # Replace the base experience
    new_base_exp = f"db {base_exp.get()} ; base exp"
    content = re.sub(base_exp_pattern, new_base_exp, content)

    # Replace the gender ratio
    new_gender_ratio = f"db {gender_ratio.get()} ; gender ratio"
    content = re.sub(gender_ratio_pattern, new_gender_ratio, content)

    # Save the modified content back to the file
    with open(file_path, 'w') as file:
        file.write(content)

    status_label.config(text=f"Saved changes to {pokemon_name}.asm")

# Create the main window
root = tk.Tk()
root.title("Pokémon Base Stats Editor")

# Variables to hold the Pokémon stats and other data
hp = tk.StringVar()
attack = tk.StringVar()
defense = tk.StringVar()
speed = tk.StringVar()
special_attack = tk.StringVar()
special_defense = tk.StringVar()
primary_type = tk.StringVar()
secondary_type = tk.StringVar()
catch_rate = tk.StringVar()
base_exp = tk.StringVar()
gender_ratio = tk.StringVar()

# Get the list of Pokémon files in the folder
pokemon_files = [f.split('.')[0] for f in os.listdir(folder_path) if f.endswith(".asm")]

# Dropdown menu to select Pokémon
pokemon_dropdown = ttk.Combobox(root, values=pokemon_files)
pokemon_dropdown.set("Select a Pokémon")
pokemon_dropdown.pack(pady=10)

# Function to load data when a Pokémon is selected
pokemon_dropdown.bind("<<ComboboxSelected>>", lambda e: load_pokemon_data(pokemon_dropdown.get()))

# Labels and entry fields for editing Pokémon stats
tk.Label(root, text="HP:").pack()
tk.Entry(root, textvariable=hp).pack()

tk.Label(root, text="Attack:").pack()
tk.Entry(root, textvariable=attack).pack()

tk.Label(root, text="Defense:").pack()
tk.Entry(root, textvariable=defense).pack()

tk.Label(root, text="Speed:").pack()
tk.Entry(root, textvariable=speed).pack()

tk.Label(root, text="Special Attack:").pack()
tk.Entry(root, textvariable=special_attack).pack()

tk.Label(root, text="Special Defense:").pack()
tk.Entry(root, textvariable=special_defense).pack()

tk.Label(root, text="Primary Type:").pack()
tk.Entry(root, textvariable=primary_type).pack()

tk.Label(root, text="Secondary Type:").pack()
tk.Entry(root, textvariable=secondary_type).pack()

tk.Label(root, text="Catch Rate:").pack()
tk.Entry(root, textvariable=catch_rate).pack()

tk.Label(root, text="Base EXP:").pack()
tk.Entry(root, textvariable=base_exp).pack()

tk.Label(root, text="Gender Ratio:").pack()
tk.Entry(root, textvariable=gender_ratio).pack()

# Save button
save_button = tk.Button(root, text="Save", command=save_pokemon_data)
save_button.pack(pady=10)

# Status label to show save status
status_label = tk.Label(root, text="")
status_label.pack(pady=5)

# Start the GUI loop
root.mainloop()
