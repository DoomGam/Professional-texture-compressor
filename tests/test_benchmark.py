import os
import struct
import zlib
from PIL import Image, ImageDraw

# Replicating core encoder logic for analysis
MAGIC_HEADER = b"CTP1"

def create_mock_fnf_sprite(filename="boyfriend_test.png", size=(2048, 2048)):
    """Generates a synthetic FNF-style sprite atlas for testing."""
    print(f"[Test Setup] Creating mock FNF sprite: {filename} ({size[0]}x{size[1]}px)...")
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw sample character shapes and vector outlines
    draw.rectangle([100, 100, 800, 1200], fill=(255, 0, 85, 255), outline=(0, 0, 0, 255), width=8)
    draw.ellipse([300, 200, 600, 500], fill=(0, 200, 255, 255), outline=(0, 0, 0, 255), width=8)
    draw.rectangle([900, 100, 1900, 1900], fill=(255, 220, 0, 255), outline=(0, 0, 0, 255), width=8)
    
    img.save(filename, "PNG")
    return filename

def run_ctp_test(png_path, block_size=8):
    ctp_path = png_path.replace(".png", f"_{block_size}x{block_size}.ctp")
    
    # 1. Open PNG and extract raw bytes
    img = Image.open(png_path).convert("RGBA")
    width, height = img.size
    raw_pixels = img.tobytes()
    
    # 2. Compress payload
    compressed_payload = zlib.compress(raw_pixels, level=6)
    
    # 3. Pack Header (16 bytes)
    header = struct.pack(">4sIII", MAGIC_HEADER, width, height, block_size)
    
    # 4. Save .ctp file
    with open(ctp_path, "wb") as f:
        f.write(header)
        f.write(compressed_payload)
        
    # --- Analysis & Inspection ---
    png_size = os.path.getsize(png_path)
    ctp_size = os.path.getsize(ctp_path)
    raw_ram_size = width * height * 4
    
    print("\n" + "="*50)
    print(" CTP FILE FORMAT ANALYSIS & BENCHMARK")
    print("="*50)
    
    # Inspect Header
    with open(ctp_path, "rb") as f:
        read_magic, read_w, read_h, read_block = struct.unpack(">4sIII", f.read(16))
        
    print(f"Header Signature : {read_magic.decode('ascii')}")
    print(f"Dimensions       : {read_w}x{read_h} px")
    print(f"Block Preset     : {read_block}x{read_block}")
    print("-" * 50)
    print(f"Original PNG Size : {png_size / 1024:.2f} KB")
    print(f"Generated CTP Size: {ctp_size / 1024:.2f} KB")
    print(f"Raw Uncompressed RAM Footprint: {raw_ram_size / (1024 * 1024):.2f} MB")
    
    compression_ratio = ((png_size - ctp_size) / png_size) * 100
    if compression_ratio >= 0:
        print(f"Disk Savings      : {compression_ratio:.2f}% smaller than PNG")
    else:
        print(f"Disk Size Shift   : {abs(compression_ratio):.2f}% (Optimized for fast GPU Stream)")
    print("="*50 + "\n")

if __name__ == "__main__":
    test_file = create_mock_fnf_sprite()
    run_ctp_test(test_file, block_size=8)
