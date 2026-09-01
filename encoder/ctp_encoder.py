import os
import struct
import zlib
from PIL import Image

MAGIC_HEADER = b"CTP2"

def pad_image_to_block_size(img, block_size):
    """
    Garante que a largura e altura da imagem sejam múltiplos exatos do block_size.
    Evita quebras de matriz e blocos corrompidos nas bordas do sprite.
    """
    width, height = img.size
    new_width = ((width + block_size - 1) // block_size) * block_size
    new_height = ((height + block_size - 1) // block_size) * block_size

    if new_width == width and new_height == height:
        return img

    padded_img = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
    padded_img.paste(img, (0, 0))
    return padded_img

def sanitize_alpha(img):
    """
    Limpa o canal de transparência: se o Alpha for muito baixo, 
    força para 0 puro para evitar blocos com ruído de cor no fundo.
    """
    r, g, b, a = img.split()
    a = a.point(lambda p: 0 if p < 5 else p)
    return Image.merge("RGBA", (r, g, b, a))

def compress_png_to_ctp(input_png_path, output_ctp_path, block_size=8, mode=0):
    """
    Encoder CTP v2 (Com Proteção Anti-Artefato/Bloquinhos Falhados)
    """
    try:
        img = Image.open(input_png_path).convert("RGBA")
        
        img = sanitize_alpha(img)
        
        img = pad_image_to_block_size(img, block_size)
        width, height = img.size
        
        if mode == 1:
            alpha_channel = img.split()[3]
            rgb_img = img.convert("RGB").quantize(colors=255, method=Image.Quantize.FASTOCTREE)
            
            quantized_rgba = rgb_img.convert("RGBA")
            quantized_rgba.putalpha(alpha_channel)
            raw_pixels = quantized_rgba.tobytes()
            compression_flag = 1
        else:
            raw_pixels = img.tobytes()
            compression_flag = 0
            
        compressed_payload = zlib.compress(raw_pixels, level=9)
        
        padding = b"\x00\x00\x00"
        header = struct.pack(">4sIIIB3s", MAGIC_HEADER, width, height, block_size, compression_flag, padding)
        
        with open(output_ctp_path, "wb") as f:
            f.write(header)
            f.write(compressed_payload)
            
        print(f"[CTP Encoder] Convertido com sucesso (Sem artefatos): {os.path.basename(input_png_path)} ({width}x{height}px)")
        return True
    except Exception as e:
        print(f"[CTP Encoder] Erro ao converter {input_png_path}: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        input_png = sys.argv[1]
        output_ctp = sys.argv[2]
        bsize = int(sys.argv[3]) if len(sys.argv) > 3 else 8
        m = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        compress_png_to_ctp(input_png, output_ctp, bsize, m)
    else:
        print("Uso: python ctp_encoder.py <input_png> <output_ctp> [block_size] [mode]")
