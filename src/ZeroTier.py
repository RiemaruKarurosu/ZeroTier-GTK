import requests
import subprocess
import psutil


#
# ZeroTier Class
# API version: 0.1.0
#

class ZeroTierNetwork:
    COMMANDS = ('start', 'stop', 'enable', 'disable')
    URL = 'http://localhost:9993/'

    def __init__(self, api_token=None):
        self.api_token = api_token
        self.serviceStatus = None
        self.listNetworks = []
        if api_token:
            self.headers = {'X-ZT1-Auth': f'{api_token}'}

    ## ZeroTier Status:

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

    # Get the Token to use ZeroTierOne Service
    def getToken(self):
        try:
            cmd = ['pkexec', 'cat', '/var/lib/zerotier-one/authtoken.secret']
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            clave_api = result.stdout.strip()
            print(f'Saving API: {clave_api}')
            self.api_token = clave_api
            self.headers = {'X-ZT1-Auth': f'{self.api_token}'}
        except subprocess.CalledProcessError:
            print('Error[01]: MissingRootAdmin')

        # ListNetworks

    def getNetworks(self, network=None):
        if network:
            url = self.URL + 'network/' + network
        else:
            url = self.URL + 'network'
        response = requests.get(url, headers=self.headers)
        return response

    def joinNetworks(self, network):
        url = self.URL + 'network' + network
        response = requests.post(url, headers=self.headers)
        print(response)
        return response

    def leaveNetworks(self, network):
        url = self.URL + 'network' + network
        response = requests.delete(url, headers=self.headers)
        print(response)
        return response
        url = self.URL + 'network' + network
        # Peers

    def getPeers(self, network=None):
        if network:
            url = self.URL + 'peer/' + network
        else:
            url = self.URL + 'peer'
        response = requests.get(url, headers=self.headers)
        print(response)
        return response
