import os
import sys
from ctp_encoder import compress_png_to_ctp

PRESET_FILES = {
    "4x4.ctp": 4,
    "6x6.ctp": 6,
    "8x8.ctp": 8,
    "10x10.ctp": 10
}

def scan_and_process_assets(assets_dir="assets"):
    """
    Escaneia o diretório de assets do jogo. Se encontrar um arquivo de configuração 
    de bloco (ex: 8x8.ctp), converte automaticamente todos os .png daquela pasta.
    """
    if not os.path.exists(assets_dir):
        print(f"[CTP Builder] Aviso: Diretório '{assets_dir}' não encontrado. Pulando automação.")
        return

    converted_count = 0

    for root, dirs, files in os.walk(assets_dir):
        active_block_size = None
        for preset_name, block_size in PRESET_FILES.items():
            if preset_name in files:
                active_block_size = block_size
                break

        if active_block_size is not None:
            for file in files:
                if file.lower().endswith(".png"):
                    png_path = os.path.join(root, file)
                    ctp_path = os.path.splitext(png_path)[0] + ".ctp"
                    
                    success = compress_png_to_ctp(png_path, ctp_path, block_size=active_block_size, mode=0)
                    if success:
                        converted_count += 1

    print(f"\n[CTP Builder] Processamento concluído! Total de texturas .ctp geradas: {converted_count}\n")

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "assets"
    print(f"[CTP Builder] Iniciando varredura automatizada em: {target_dir}")
    scan_and_process_assets(target_dir)
