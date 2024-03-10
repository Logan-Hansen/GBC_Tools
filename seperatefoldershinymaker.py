import os
from PIL import Image

def apply_palette(image_path, palette_path, output_folder):
    # Open the image
    img = Image.open(image_path)
    
    # Open the palette file
    with open(palette_path, 'r') as f:
        # Skip the first line
        f.readline()
        # Read the RGB values for A and B
        rgb_values = []
        for _ in range(2):
            line = f.readline().strip()
            try:
                # Extract RGB values and scale them by 8
                rgb = [int(value.strip()) * 8 for value in line.split("RGB")[1].split(",")]
                rgb_values.append(rgb)
            except ValueError as e:
                print(f"Error parsing RGB values: {e}")
                return
    
    # Convert the image to "P" mode (palette-based) if it's not already in that mode
    if img.mode != "P":
        img = img.convert("P")
    
    # Get the palette
    palette = img.getpalette()
    
    # Replace the second and third colors in the palette with the RGB values from the palette file
    palette[3:6] = rgb_values[0]  # Second color
    palette[6:9] = rgb_values[1]  # Third color
    
    # Apply the modified palette to the image
    img.putpalette(palette)
    
    # Construct the output filename
    folder_name = os.path.basename(os.path.dirname(image_path))
    output_filename = os.path.join(output_folder, folder_name + "_" + os.path.basename(image_path))
    
    # Save the modified image to the output folder
    img.save(output_filename)

def process_folder(folder_path, output_folder):
    # List all files in the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            # Process the file if it's a PNG image
            if item.endswith('.png'):
                palette_file = os.path.join(folder_path, "shiny.pal")
                if os.path.exists(palette_file):
                    print(f"Applying palette for {item}")
                    print(f"Palette file: {palette_file}")
                    apply_palette(item_path, palette_file, output_folder)
                else:
                    print(f"No palette file found for {item}")

# Path to the main folder containing subdirectories with images
main_folder_path = "files"
output_folder = os.path.join(main_folder_path, "../output")

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each subdirectory within the main folder
for subfolder in os.listdir(main_folder_path):
    subfolder_path = os.path.join(main_folder_path, subfolder)
    if os.path.isdir(subfolder_path):
        print(f"Processing folder: {subfolder}")
        process_folder(subfolder_path, output_folder)
