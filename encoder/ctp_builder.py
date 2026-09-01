import os
import json
import sys

# Supported CTP block preset files
BLOCK_PRESETS = ["4x4.ctp", "6x6.ctp", "8x8.ctp", "10x10.ctp"]

def find_and_process_folders(assets_dir):
    """
    Scans the assets directory for block preset files and triggers texture compression.
    """
    print("[CTP Builder] Scanning assets for .ctp block configuration files...")
    
    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            if file in BLOCK_PRESETS:
                config_path = os.path.join(root, file)
                print(f"[CTP Builder] Found configuration '{file}' in folder: {root}")
                
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        
                    block_size = config.get("blockSize", 8)
                    print(f"[CTP Builder] Applying CTP Block Size: {block_size}x{block_size} for directory: {root}")
                    
                    compress_folder_textures(root, block_size, config)
                except Exception as e:
                    print(f"[CTP Builder] Error reading {config_path}: {e}")

def compress_folder_textures(folder_path, block_size, config):
    """
    Compresses all PNG textures found in the specified folder into .ctp format.
    """
    for file in os.listdir(folder_path):
        if file.lower().endswith(".png"):
            png_path = os.path.join(folder_path, file)
            output_ctp = os.path.join(folder_path, os.path.splitext(file)[0] + ".ctp")
            
            print(f"[CTP Builder] Compressing: {file} -> {os.path.basename(output_ctp)} (Block: {block_size}x{block_size})")
            # Compression engine call will be linked here in the next step

if __name__ == "__main__":
    # Target directory defaults to assets if not provided by Lime build hook
    target_assets = sys.argv[1] if len(sys.argv) > 1 else "assets"
    
    if os.path.exists(target_assets):
        find_and_process_folders(target_assets)
    else:
        print(f"[CTP Builder] Directory '{target_assets}' not found. Skipping scan.")
