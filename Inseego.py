import requests
from bs4 import BeautifulSoup
import hashlib
import bcrypt
import re
import json

class InseegoDevice:
    def __init__(self, address):
        self.url = 'http://' + address
        self.session = requests.Session()

    def get_soup(self, path):
        page = self.session.get(self.url + path)

        if not page.status_code == 200:
            raise Exception('bad response to login: %d' % (page.status_code))

        return(BeautifulSoup(page.content, "html.parser"))

    def authenticate(self, password):
        raise NotImplementedError("Subclasses must implement authenticate method")

    def restart(self):
        token = re.search('gSecureToken : "([^"]+)"', self.get_soup('/restarting').decode()).group(1)

        page = self.session.post(
            self.url + '/restarting/reboot',
            data={
                'gSecureToken': token,
            },
        )
        if not page.status_code == 200:
            raise Exception('failed to restart')

    def status(self):
        page = self.session.get(self.url + '/srv/status')

        if not page.status_code == 200:
            raise Exception('failed to retrieve status')

        return(json.loads(page.content))

class M3000(InseegoDevice):
    def __init__(self, address):
        super().__init__(address)
        self.salt_prefix = b'2a'
        self.salt_rounds = 10
        self.salt_len = 16

    def authenticate(self, password):
        token = self.get_soup('/login').find('input', { 'id':"gSecureToken"})['value']

        output = bcrypt._bcrypt.ffi.new("char[]", 30)
        bcrypt._bcrypt.lib.encode_base64(output, bytes(token, 'utf-8')[:self.salt_len], self.salt_len)
        salt = b"$" + self.salt_prefix + b"$" + ("%2.2u" % self.salt_rounds).encode("ascii") + b"$" + bcrypt._bcrypt.ffi.string(output)

        page = self.session.post(
            self.url + '/submitLogin/',
            data={
                'shaPassword': bcrypt.hashpw(password.encode('utf-8'), salt),
                'gSecureToken': token,
            },
        )
        if not page.status_code == 200:
            raise Exception('authentication failure')

class FX2000(InseegoDevice):
    def __init__(self, address):
        super().__init__(address)

    def authenticate(self, password):
        token = self.get_soup('/login').find('input', { 'id':"gSecureToken"})['value']
        
        # Combine the password with the security token
        combined = password + token
        
        # Compute the SHA-1 hash of the combined string
        sha_password = hashlib.sha1(combined.encode()).hexdigest()

        page = self.session.post(
            self.url + '/submitLogin/',
            data={
                'shaPassword': sha_password,
                'gSecureToken': token,
            },
        )
        if not page.status_code == 200:
            raise Exception('authentication failure')
