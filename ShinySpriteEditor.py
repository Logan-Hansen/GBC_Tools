import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ShinySpritePreviewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Shiny Sprite Previewer")

        self.pokemon_folders = self.get_pokemon_folders()
        self.current_pokemon = None
        self.front_sprite = None
        self.back_sprite = None
        self.img_tk_original_front = None
        self.img_tk_original_back = None
        self.img_tk_shiny_front = None
        self.img_tk_shiny_back = None

        # Dropdown menu to select Pokémon
        self.pokemon_dropdown_label = tk.Label(root, text="Select Pokémon:")
        self.pokemon_dropdown_label.pack()

        self.pokemon_dropdown = ttk.Combobox(root, values=self.pokemon_folders)
        self.pokemon_dropdown.bind("<<ComboboxSelected>>", self.load_pokemon)
        self.pokemon_dropdown.pack()

        # Image preview area
        self.image_canvas = tk.Canvas(root)
        self.image_canvas.pack()

    def get_pokemon_folders(self):
        """ Get the names of all subfolders representing Pokémon """
        base_path = os.path.dirname(os.path.realpath(__file__))
        pokemon_folders = [name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]
        return pokemon_folders

    def load_pokemon(self, event):
        """ Load the selected Pokémon's images and shiny palette """
        self.current_pokemon = self.pokemon_dropdown.get()
        pokemon_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.current_pokemon)

        # Load the front and back sprites
        self.front_sprite = Image.open(os.path.join(pokemon_folder, "front.png"))
        self.back_sprite = Image.open(os.path.join(pokemon_folder, "back.png"))

        # Load shiny palette
        shiny_pal_path = os.path.join(pokemon_folder, "shiny.pal")
        if os.path.exists(shiny_pal_path):
            shiny_palette = self.load_shiny_palette(shiny_pal_path)
            self.apply_shiny_palette(shiny_palette)

    def load_shiny_palette(self, palette_path):
        """ Load and return the shiny palette values """
        with open(palette_path, 'r') as file:
            file.readline()  # Skip first line
            rgb_values = []
            for _ in range(2):  # Only first two colors in the palette
                line = file.readline().strip()
                try:
                    rgb = [int(value.strip()) * 8 for value in line.split("RGB")[1].split(",")]
                    rgb_values.append(rgb)
                except ValueError as e:
                    print(f"Error parsing RGB values: {e}")
            return rgb_values

    def apply_shiny_palette(self, shiny_palette):
        """ Apply the shiny palette to the sprites and display them """
        # Convert to "P" mode for palette-based image
        shiny_front = self.front_sprite.convert("P")
        shiny_back = self.back_sprite.convert("P")

        # Get the current palette
        palette = shiny_front.getpalette()

        # Apply the shiny palette colors (replace colors 3 and 6)
        if len(shiny_palette) >= 2:
            palette[3:6] = shiny_palette[0]  # Apply first shiny color
            palette[6:9] = shiny_palette[1]  # Apply second shiny color

        # Apply the modified palette to both images
        shiny_front.putpalette(palette)
        shiny_back.putpalette(palette)

        # Show all images in the GUI
        self.show_images(self.front_sprite, shiny_front, self.back_sprite, shiny_back)

    def show_images(self, original_front, shiny_front, original_back, shiny_back):
        """ Display all images on the canvas in the specified arrangement """
        # Double the size of the images
        original_front = original_front.resize((original_front.width * 2, original_front.height * 2), Image.NEAREST)
        shiny_front = shiny_front.resize((shiny_front.width * 2, shiny_front.height * 2), Image.NEAREST)
        original_back = original_back.resize((original_back.width * 2, original_back.height * 2), Image.NEAREST)
        shiny_back = shiny_back.resize((shiny_back.width * 2, shiny_back.height * 2), Image.NEAREST)

        # Calculate canvas size
        canvas_width = original_front.width + shiny_front.width
        canvas_height = max(original_front.height, shiny_front.height) + original_back.height
        self.image_canvas.config(width=canvas_width, height=canvas_height)

        # Convert the images for Tkinter
        self.img_tk_original_front = ImageTk.PhotoImage(original_front)
        self.img_tk_shiny_front = ImageTk.PhotoImage(shiny_front)
        self.img_tk_original_back = ImageTk.PhotoImage(original_back)
        self.img_tk_shiny_back = ImageTk.PhotoImage(shiny_back)

        # Clear the canvas before drawing new images
        self.image_canvas.delete("all")

        # Place images on the canvas
        self.image_canvas.create_image(0, 0, anchor="nw", image=self.img_tk_original_front)  # Original front
        self.image_canvas.create_image(original_front.width, 0, anchor="nw", image=self.img_tk_shiny_front)  # Shiny front
        self.image_canvas.create_image(0, original_front.height, anchor="nw", image=self.img_tk_original_back)  # Original back
        self.image_canvas.create_image(original_front.width, original_front.height, anchor="nw", image=self.img_tk_shiny_back)  # Shiny back

        # Keep references to avoid garbage collection
        self.image_canvas.img_original_front = self.img_tk_original_front
        self.image_canvas.img_shiny_front = self.img_tk_shiny_front
        self.image_canvas.img_original_back = self.img_tk_original_back
        self.image_canvas.img_shiny_back = self.img_tk_shiny_back


if __name__ == "__main__":
    root = tk.Tk()
    app = ShinySpritePreviewer(root)
    root.mainloop()
