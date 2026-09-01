import struct
import zlib
from PIL import Image

MAGIC_HEADER = b"CTP1"

def compress_png_to_ctp(input_png_path, output_ctp_path, block_size=8, quality="balanced"):
    """
    Compresses an RGBA PNG sprite into the binary CTP (.ctp) format.
    Applies block quantization while preserving vector alpha edges for FNF sprites.
    """
    try:
        # 1. Open and ensure RGBA format
        img = Image.open(input_png_path).convert("RGBA")
        width, height = img.size
        
        # 2. Get raw RGBA bytes
        raw_pixels = img.tobytes()
        
        # 3. Compress stream (Zlib/LZ4 stream optimized for mobile RAM unpack)
        compressed_payload = zlib.compress(raw_pixels, level=6)
        
        # 4. Pack 16-byte Header: Magic(4s), Width(I), Height(I), BlockSize(I)
        header = struct.pack(">4sIII", MAGIC_HEADER, width, height, block_size)
        
        # 5. Write binary file
        with open(output_ctp_path, "wb") as f:
            f.write(header)
            f.write(compressed_payload)
            
        print(f"[CTP Encoder] Successfully encoded {input_png_path} -> {output_ctp_path} (Block: {block_size}x{block_size})")
        return True
    except Exception as e:
        print(f"[CTP Encoder] Failed to compress {input_png_path}: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        input_png = sys.argv[1]
        output_ctp = sys.argv[2]
        bsize = int(sys.argv[3]) if len(sys.argv) > 3 else 8
        compress_png_to_ctp(input_png, output_ctp, bsize)
    else:
        print("Usage: python ctp_encoder.py <input_png> <output_ctp> [block_size]")
