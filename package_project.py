import os
import zipfile

def create_ctp_zip(output_filename="Compressor-Texture-Profissioner.zip"):
    EXCLUDE_DIRS = {'.git', '__pycache__', '.vscode', '.idea'}
    EXCLUDE_FILES = {output_filename, 'package_project.py'}

    project_root = os.getcwd()
    print(f"[Package] Compactando o projeto em '{output_filename}'...")

    file_count = 0
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_root):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                if file in EXCLUDE_FILES or file.endswith('.pyc'):
                    continue

                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, project_root)
                
                zipf.write(full_path, relative_path)
                print(f"  + Adicionado: {relative_path}")
                file_count += 1

    print(f"\n[SUCESSO] Pacote gerado com sucesso! Total de arquivos: {file_count}")
    print(f"Arquivo gerado: {os.path.abspath(output_filename)}\n")

if __name__ == "__main__":
    create_ctp_zip()
