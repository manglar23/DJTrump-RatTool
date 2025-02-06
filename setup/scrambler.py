import sys
import os
from notoken887.encryptor import TokenCryptor
import base64

def obf():
    if len(sys.argv) != 3:
        print("Error: Please provide both input and output folder names.")
        return
    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    c = TokenCryptor()

    for root, _, files in os.walk(input_folder):
        output_subfolder = os.path.join(output_folder, os.path.relpath(root, input_folder))
        if not os.path.exists(output_subfolder):
            os.makedirs(output_subfolder)

        for file in files:
            if file.endswith(".py"):
                input_file_path = os.path.join(root, file)
                output_file_path = os.path.join(output_subfolder, file)

                with open(input_file_path, 'r', encoding='utf-8') as infile:
                    code = infile.readlines()

                import_lines = [line for line in code if line.strip().startswith(("from", "import"))]
                code_lines = [line for line in code if not line.strip().startswith(("from", "import"))]

                import_code = "\n".join(import_lines)
                code_to_obfuscate = ''.join(code_lines)
                first_base64 = base64.b64encode(code_to_obfuscate.encode('utf-8')).decode('utf-8')
                second_base64 = base64.b64encode(first_base64.encode('utf-8')).decode('utf-8')
                obfuscated_code = c.proccess(second_base64)
                obfuscated_code = ''.join([char for char in obfuscated_code if char != '\x00'])
                obfuscated_module_code = f"""
{import_code}
from notoken887.encryptor import TokenCryptor
import base64
obfuscatedheader='''{obfuscated_code}'''
def print(code):
    exec(code)
FFGSHSGHYUFYUHFUIHEUIHEUIH432894ue8i = TokenCryptor()
FEBUFHBEUYFUEHFIUEHNFIUHUIFHIe47e4e45e = '''{obfuscated_code}'''
GFEBUFHBEUYFUEHFIUEGNFIUHUIFHIe47e4e45e = FFGSHSGHYUFYUHFUIHEUIHEUIH432894ue8i.process(FEBUFHBEUYFUEHFIUEHNFIUHUIFHIe47e4e45e)
GFEBUFHBEUYFUEHFIUEHNFIUHUIFHIe47e4e45e = base64.b64decode(base64.b64decode(GFEBUFHBEUYFUEHFIUEGNFIUHUIFHIe47e4e45e)).decode('utf-8')
exec(GFEBUFHBEUYFUEHFIUEHNFIUHUIFHIe47e4e45e)
"""
                with open(output_file_path, 'w', encoding='utf-8') as outfile:
                    outfile.write(obfuscated_module_code)
obf() 