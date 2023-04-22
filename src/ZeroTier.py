import requests
import subprocess
import psutil
import os
from pathlib import Path


#
# ZeroTier Class
# API version: 0.1.0
#

class ZeroTierNetwork:
    COMMANDS = ('start', 'stop', 'enable', 'disable')
    URL = 'http://localhost:9993/'
    PATH = Path.home() / '.config' / 'ztlib'
    FILE = 'zt.conf'

    def __init__(self, api_token=None):
        self.api_token = api_token
        self.serviceStatus = None
        self.listNetworks = []
        if api_token:
            self.headers = {'X-ZT1-Auth': f'{api_token}'}
        else:
            self.headers = None

    def ztStart(self) -> str:
        if not self.checkToken(self.api_token):
            if self.readToken() == 401 or self.readToken() == 404:
                if self.checkToken(self.getToken()):
                    return 'OK'
                else:
                    return 'MISSING ROOT PERMISSION'
            return 'OK'
        return 'OK'

        # ZeroTier Status:

    # Check if ZeroTier-One is active
    def ztStatus(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if 'zerotier-one' in proc.info['name']:
                return True
        return False

    # Change ZeroTier-One service
    def service(self, setstatus):
        if setstatus:
            self.serviceStatus = self.COMMANDS[setstatus - 1]
            self._ztActivate()

    def _ztActivate(self):
        result = subprocess.run(['pkexec', 'systemctl', self.serviceStatus, 'zerotier-one.service'],
                                capture_output=True, text=True)
        if result.returncode == 0:
            print('Servicio de ZeroTier iniciado exitosamente.')
        else:
            print('Error al iniciar el servicio de ZeroTier:', result.stderr.strip())
        self.serviceStatus = None

    # Save apiToken to ~/.config
    def readToken(self) -> int:
        configpath = self.PATH / self.FILE
        if configpath.exists():
            with open(configpath, 'r') as configfile:
                apitoken = configfile.readlines()
            for token in apitoken:
                if token.startswith('X-ZT1-Auth'):
                    key, value = token.split('=')
                    api_token = value.strip()
                    if self.checkToken(api_token):
                        self.api_token = api_token
                        self.headers = {'X-ZT1-Auth': f'{api_token}'}
                    else:
                        return 401
            return 200
        else:
            return 404

    def checkToken(self, api_token):
        url = self.URL + 'status'
        header = {'X-ZT1-Auth': f'{api_token}'}
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return True
        elif response.status_code == 401:
            return False
        else:
            return False

    def saveToken(self):
        if not self.PATH.exists():
            self.PATH.mkdir(parents=True)
        configpath = self.PATH / self.FILE
        if not configpath.exists():
            configpath.touch()

        with open(configpath, 'w') as configfile:
            configfile.write(f'X-ZT1-Auth = {self.api_token} \n')

        os.chmod(configpath, 0o600)
        print(configpath)

    # Get the Token to use ZeroTierOne Service
    def getToken(self):
        try:
            cmd = ['pkexec', 'cat', '/var/lib/zerotier-one/authtoken.secret']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            clave_api = result.stdout.strip()
            print(f'Saving API: {clave_api}')
            if self.checkToken(clave_api):
                self.api_token = clave_api
                self.headers = {'X-ZT1-Auth': f'{self.api_token}'}
                self.saveToken()
                return clave_api
        except subprocess.CalledProcessError:
            return 'Error[01]: MissingRootAdmin'

        # ListNetworks

    def getNetworks(self, network=None):
        if network:
            url = self.URL + 'network/' + network
        else:
            url = self.URL + 'network'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def joinNetworks(self, network):
        url = self.URL + 'network' + network
        response = requests.post(url, headers=self.headers)
        print(response.json())
        return response.json()

    def updateNetwork(self, network, config):
        # Version 2.0 plan.
        pass
    def leaveNetworks(self, network):
        url = self.URL + 'network' + network
        response = requests.delete(url, headers=self.headers)
        print(response)
        return response
        # Peers

    def getPeers(self, network=None):
        if network:
            url = self.URL + 'peer/' + network
        else:
            url = self.URL + 'peer'
        response = requests.get(url, headers=self.headers)
        print(response.json())
        return response.json()

