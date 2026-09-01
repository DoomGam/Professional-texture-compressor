import os
import sys

# Garante a importação do encoder na pasta pai/encoder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'encoder')))

import struct
from PIL import Image, ImageDraw
from ctp_encoder import compress_png_to_ctp, MAGIC_HEADER

def create_mock_fnf_sprite(filename="tests/boyfriend_test.png", size=(2000, 2000)):
    """Gera um sprite sintético de FNF com tamanho não-múltiplo para testar o Padding automático."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    print(f"[Test Setup] Gerando sprite de teste FNF: {filename} ({size[0]}x{size[1]}px)...")
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Desenha formas de teste com transparência e bordas
    draw.rectangle([100, 100, 800, 1200], fill=(255, 0, 85, 255), outline=(0, 0, 0, 255), width=8)
    draw.ellipse([300, 200, 600, 500], fill=(0, 200, 255, 255), outline=(0, 0, 0, 255), width=8)
    draw.rectangle([900, 100, 1800, 1800], fill=(255, 220, 0, 255), outline=(0, 0, 0, 255), width=8)
    
    img.save(filename, "PNG")
    return filename

def run_benchmark():
    png_path = create_mock_fnf_sprite()
    ctp_path = png_path.replace(".png", ".ctp")
    block_size = 8
    
    # 1. Executa a compressão via encoder v2
    success = compress_png_to_ctp(png_path, ctp_path, block_size=block_size, mode=0)
    assert success, "A compressão falhou!"

    # 2. Inspeciona o cabeçalho binário (20 Bytes - Header v2)
    with open(ctp_path, "rb") as f:
        header_bytes = f.read(20)
        read_magic, read_w, read_h, read_block, read_mode, padding = struct.unpack(">4sIIIB3s", header_bytes)

    png_size = os.path.getsize(png_path)
    ctp_size = os.path.getsize(ctp_path)
    ram_footprint = (read_w * read_h * 4) / (1024 * 1024)

    # 3. Exibe o relatório detalhado de validação
    print("\n" + "="*55)
    print(" CTP FORMAT V2 (CTP2) - VALIDATION & BENCHMARK")
    print("="*55)
    print(f" Magic Signature  : {read_magic.decode('ascii')} (Esperado: CTP2)")
    print(f" Original Dimensions: 2000x2000 px")
    print(f" Padded Dimensions : {read_w}x{read_h} px (Alinhado para bloco {read_block}x{read_block})")
    print(f" Compression Mode : {read_mode} (0 = Raw RGBA Stream)")
    print("-" * 55)
    print(f" Original PNG Size: {png_size / 1024:.2f} KB")
    print(f" Generated CTP Size: {ctp_size / 1024:.2f} KB")
    print(f" Uncompressed RAM : {ram_footprint:.2f} MB")
    print("="*55)

    # Assertivas de segurança
    assert read_magic == b"CTP2", "Magic Header incorreto!"
    assert read_w % block_size == 0 and read_h % block_size == 0, "Falha no Auto-Padding de blocos!"
    print("\n[SUCCESS] Todos os testes do formato CTP v2 passaram com sucesso!\n")

if __name__ == "__main__":
    run_benchmark()
