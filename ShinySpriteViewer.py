from PIL import Image
import os

# This program requires you to have a shiny.pal file in the same folder as the png image you want to apply it to
# The .pal file should be formatted like the example below (including the empty line to start and the tabs):


#
#	RGB 27, 20, 13
#	RGB 25, 15, 00
#
#


def apply_palette(image_path, palette_path):
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
    
    # Save the modified image to disk for inspection
    output_path = os.path.splitext(image_path)[0] + "_modified.png"
    img.save(output_path)

# Add these lines back in if you want it to open the image for you to see as soon as its done. Makes it much slower.    
#    # Check if the image mode is supported for display
#    if img.mode in ['1', 'L', 'RGB', 'RGBA']:
#        # Display the image
#        img.show()
#    else:
#        print(f"Image mode '{img.mode}' not supported for display. Converted to 'RGB' for display.")
#        # Convert the image to 'RGB' mode for display
#        img.convert("RGB").show()

def process_folder(folder_path):
    # List all files and subdirectories in the folder
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            # Process the file if it's a PNG image
            if item.endswith('.png'):
                palette_file = os.path.join(folder_path, "shiny.pal")
                if os.path.exists(palette_file):
                    print(f"Applying palette for {item}")
                    print(f"Palette file: {palette_file}")
                    apply_palette(item_path, palette_file)
                else:
                    print(f"No palette file found for {item}")
        elif os.path.isdir(item_path):
            # Recursively process subdirectories
            process_folder(item_path)

# Path to the main folder containing subdirectories with images
main_folder_path = "files"

# Process each subdirectory within the main folder
for subfolder in os.listdir(main_folder_path):
    subfolder_path = os.path.join(main_folder_path, subfolder)
    if os.path.isdir(subfolder_path):
        print(f"Processing folder: {subfolder}")
        process_folder(subfolder_path)
