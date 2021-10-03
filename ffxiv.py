from urllib.error import HTTPError
from datetime import datetime
from parsel import Selector
from time import sleep
import requests
import urllib.request
import ctypes

def send_to_telegram(state, id):
    bot_token = '1880341910:AAGn4vFUhun8r_0IK4pwJ4dZtWf5woyJ7jE'
    userID = id
    message = f'Behemoth character creation: {"Available! 🟢🟢🟢" if state else "Blocked! 🔴🔴🔴"}'

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    data = {'chat_id': userID, 'text': message}

    requests.post(url, data)

def success():
    ctypes.windll.user32.MessageBoxW(0, "Server is now available!", "Attention!", 0x00001000)
    # send_to_telegram()

def wait_spinner(seconds):
    wait = seconds*1000
    while wait >0:
        wait -= spinner()

def spinner(intervalms=200, chars='|/-\\|'):
    elapsed = 0
    for char in chars:
        print(char, '\r', end="")
        elapsed += intervalms
        sleep(intervalms/1000)
    return elapsed

def status_request(server):
    try:
        print(datetime.now().strftime("> [%H:%M:%S] "), end="")
        print(f'Status of {server}: ', end='')
        fp = urllib.request.urlopen("https://na.finalfantasyxiv.com/lodestone/worldstatus/")

    except(HTTPError):
        print("Request error")
        return None
        
    else:
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()
        html = Selector(text=mystr)
        status = html.xpath(f'//div[@class="world-list__item" and contains(., "{server}")]//div[@class="world-list__create_character"]/i/@data-tooltip').get()
        print(f'{status.split()[-1]}')
    
    if 'Available' in status:
        return True
    return False

def print_title():
    print('\n\n')
    print(f"  _____                           _____ _               _    ")
    print(f" / ____|                         / ____| |             | |   ")
    print(f"| (___   ___ _ ____   _____ _ __| |    | |__   ___  ___| | __")
    print(f" \\___ \\ / _ \\ '__\\ \\ / / _ \\ '__| |    | '_ \\ / _ \\/ __| |/ /")
    print(f" ____) |  __/ |   \\ V /  __/ |  | |____| | | |  __/ (__|   < ")
    print(f"|_____/ \\___|_|    \\_/ \\___|_|   \\_____|_| |_|\\___|\\___|_|\\_\\")
    print('\n\n\n')

def run():
    print_title()
    
    while True:
        server = input('Type server name or hit <ENTER> for \"Behemoth\": ') or 'Behemoth'
        if server not in serverlist:
            print('Invalid server name! Try again.\n')
        else: break

    time_interval_secs = 0

    while not time_interval_secs:
        try:
            time_interval_secs = int(input("Interval between checks (seconds):" ))
            if not time_interval_secs >0: raise ValueError
        except(ValueError):
            print("Interval must be a positive integer!")

    print('\n')
    print(f'--------------------------')
    print(f' Server: {server}')
    print(f' Period: {time_interval_secs} (s)')
    print(f'--------------------------')
    print('\n\n\n')
    status = False
    while True:
        response = status_request(server)
        if (response is not None) and (not status == response):
            status = response
            send_to_telegram(status)
        wait_spinner(time_interval_secs)

serverlist = [
    'Adamantoise',
    'Cactuar',
    'Faerie',
    'Gilgamesh',
    'Jenova',
    'Midgardsormr',
    'Sargatanas',
    'Siren',
    'Balmung',
    'Brynhildr',
    'Coeurl',
    'Diabolos',
    'Goblin',
    'Malboro',
    'Mateus',
    'Zalera',
    'Behemoth',
    'Excalibur',
    'Exodus',
    'Famfrit',
    'Hyperion',
    'Lamia',
    'Leviathan',
    'Ultros',
    'Cerberus',
    'Louisoix',
    'Moogle',
    'Omega',
    'Ragnarok',
    'Spriggan',
    'Lich',
    'Odin',
    'Phoenix',
    'Shiva',
    'Twintania',
    'Zodiark',
    'Aegis',
    'Atomos',
    'Carbuncle',
    'Garuda',
    'Gungnir',
    'Kujata',
    'Ramuh',
    'Tonberry',
    'Typhon',
    'Unicorn',
    'Alexander',
    'Bahamut',
    'Durandal',
    'Fenrir',
    'Ifrit',
    'Ridill',
    'Tiamat',
    'Ultima',
    'Valefor',
    'Yojimbo',
    'Zeromus',
    'Anima',
    'Asura',
    'Belias',
    'Chocobo',
    'Hades',
    'Ixion',
    'Mandragora',
    'Masamune',
    'Pandemonium',
    'Shinryu',
    'Titan'
]

if __name__ == '__main__':
    run()