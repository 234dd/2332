import requests


class Rcon:

    def __init__(self):
        self.url = 'http://ironmine.fun/api/rcon/index.php?'

    def send(self, mode, command):
        return requests.get(url=self.url+f'mode={mode}&command={command}').text
