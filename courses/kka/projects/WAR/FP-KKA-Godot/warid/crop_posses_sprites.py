from PIL import Image
import os

def crop_image(src_path, dest_path):
    print(f"Cropping {src_path} -> {dest_path}")
    img = Image.open(src_path)
    bbox = img.getbbox()
    if bbox:
        # Crop to the bounding box
        cropped = img.crop(bbox)
        # Save the cropped image
        cropped.save(dest_path)
    else:
        print(f"Warning: {src_path} is empty!")

if __name__ == "__main__":
    src_dir = "d:/Tugas Rakha/KKA/FP/FP-KKA-Godot/warid/Asset/Assetmentah"
    dest_dir = "d:/Tugas Rakha/KKA/FP/FP-KKA-Godot/warid/Asset/Sprites"
    
    files = [
        "Posses_Blue_Armored.png",
        "Posses_Blue_Worker.png",
        "Posses_Red_Armored.png",
        "Posses_Red_Worker.png"
    ]
    
    for filename in files:
        src = os.path.join(src_dir, filename)
        dest = os.path.join(dest_dir, filename)
        if os.path.exists(src):
            crop_image(src, dest)
        else:
            print(f"File not found: {src}")
