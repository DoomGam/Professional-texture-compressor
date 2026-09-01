import os
import sys

# Garante a importação do encoder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'encoder')))

import struct
from PIL import Image, ImageDraw
from ctp_encoder import compress_png_to_ctp

def create_mock_sprite(filename, size):
    """Gera um sprite de teste com dimensões personalizadas."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Desenha um retângulo de teste
    draw.rectangle([10, 10, size[0]-10, size[1]-10], fill=(255, 0, 100, 255), outline=(0, 0, 0, 255), width=4)
    img.save(filename, "PNG")
    return filename

def test_dimensions():
    # Lista de dimensões variadas para testar o Auto-Padding
    test_cases = [
        (2048, 2048),  # Tamanho padrão FNF (Atlas Grande)
        (1024, 1024),  # Atlas Médio
        (1337, 789),   # Dimensão completamente irregular (Não potência de 2 / Impar)
        (512, 300)     # UI / Props de Estágio
    ]

    print("\n" + "="*60)
    print(" CTP FORMAT V2 (CTP2) - MULTI-DIMENSION VALIDATION TEST")
    print("="*60)

    for width, height in test_cases:
        png_path = f"tests/test_{width}x{height}.png"
        ctp_path = png_path.replace(".png", ".ctp")
        block_size = 8

        create_mock_sprite(png_path, (width, height))
        
        # Executa a compressão
        success = compress_png_to_ctp(png_path, ctp_path, block_size=block_size, mode=0)
        assert success, f"Falha na compressão para {width}x{height}!"

        # Lê e valida o cabeçalho
        with open(ctp_path, "rb") as f:
            header_bytes = f.read(20)
            read_magic, read_w, read_h, read_block, read_mode, _ = struct.unpack(">4sIIIB3s", header_bytes)

        print(f"[TEST] Original: {width}x{height}px | Padded: {read_w}x{read_h}px | Magic: {read_magic.decode('ascii')}")

        # Validações de segurança
        assert read_magic == b"CTP2", "Magic Header inválido!"
        assert read_w % block_size == 0, f"Largura {read_w} não é múltiplo do bloco {block_size}!"
        assert read_h % block_size == 0, f"Altura {read_h} não é múltiplo do bloco {block_size}!"

        # Limpeza de arquivos temporários de teste
        if os.path.exists(png_path): os.remove(png_path)
        if os.path.exists(ctp_path): os.remove(ctp_path)

    print("="*60)
    print("[SUCCESS] Todas as dimensões foram processadas e alinhadas sem erros!\n")

if __name__ == "__main__":
    test_dimensions()
