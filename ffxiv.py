from urllib.error import HTTPError
from datetime import datetime
from parsel import Selector
from time import sleep
import requests
import urllib.request as get
import ctypes

class Spinner:
    def __init__(self, intervalms=200, chars='|/-\\|'):
        self.intervalms = intervalms
        self.chars = chars

    def _idle(self):
        elapsed = 0
        for char in self.chars:
            print(char, '\r', end="")
            sleep(self.intervalms/1000)
            elapsed += self.intervalms
        return elapsed

    def wait(self, seconds):
        wait = seconds*1000
        while wait >0:
            wait -= self._idle()

class FFXIVScrapper:
    def __init__(self, server, period, telegram_id=157363763):
        self.server = server
        self.period = period
        self.telegram_id = telegram_id
        self.status = False

    def announcement(self):
        return f'{self.server} character creation: {"Available! 🟢" if self.status else "Blocked! 🔴"}'

    def send_to_telegram(self):
        bot_token = '1880341910:AAGn4vFUhun8r_0IK4pwJ4dZtWf5woyJ7jE'
        userID = str(self.telegram_id)
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
        data = {'chat_id': userID, 'text': self.announcement()}
        requests.post(url, data)

    def on_change(self):
        ctypes.windll.user32.MessageBoxW(0, self.announcement(), "Attention!", 0x00001000)
        if self.telegram_id is not None:
            self.send_to_telegram()

    def status_request(self):
        try:
            print(datetime.now().strftime("> [%H:%M:%S] "), end="")
            print(f'Status of {self.server}: ', end='')
            fp = get.urlopen("https://na.finalfantasyxiv.com/lodestone/worldstatus/")

        except(HTTPError):
            print("Request error")
            return None

        else:
            mybytes = fp.read()
            mystr = mybytes.decode("utf8")
            fp.close()
            html = Selector(text=mystr)
            status = html.xpath(f'//div[@class="world-list__item" and contains(., "{self.server}")]//div[@class="world-list__create_character"]/i/@data-tooltip').get()
            print(f'{status.split()[-1]}')

        if 'Available' in status:
            return True
        return False

    def run(self):
        spinner = Spinner()
        print('\n')
        print(f'--------------------------')
        print(f' Server: {self.server}')
        print(f' Period: {self.period} (s)')
        print(f'--------------------------')
        print('\n\n\n')
        while True:
            response = self.status_request()
            if (response is not None) and (not self.status == response):
                self.status = response
                self.on_change()
                # send_to_telegram(status)
            spinner.wait(self.period)

if __name__ == '__main__':

    time_interval_secs = 0
    id = None
    with open('serverlist.txt') as file:
        serverlist = file.read().splitlines()

    print('\n\n')
    print(f"  _____                           _____ _               _    ")
    print(f" / ____|                         / ____| |             | |   ")
    print(f"| (___   ___ _ ____   _____ _ __| |    | |__   ___  ___| | __")
    print(f" \\___ \\ / _ \\ '__\\ \\ / / _ \\ '__| |    | '_ \\ / _ \\/ __| |/ /")
    print(f" ____) |  __/ |   \\ V /  __/ |  | |____| | | |  __/ (__|   < ")
    print(f"|_____/ \\___|_|    \\_/ \\___|_|   \\_____|_| |_|\\___|\\___|_|\\_\\")
    print('\n\n\n')
    while True:
        server = input('Type server name or hit <ENTER> for \"Behemoth\": ') or 'Behemoth'
        if server not in serverlist:
            print('Invalid server name! Try again.\n')
        else: break

    while not time_interval_secs:
        try:
            time_interval_secs = int(input("Interval between checks (seconds):" ))
            if not time_interval_secs >0:
                raise ValueError
        except(ValueError):
            print("Interval must be a positive integer!")

    while id is None:
        try:
            id = input("Insert telegram ID for notification or hit <ENTER> to skip:" )
            if not isinstance(id, int) and id != '':
                raise ValueError
        except(ValueError):
            print("ID must be an integer!")

    service = FFXIVScrapper(server, time_interval_secs, id)
    service.run()