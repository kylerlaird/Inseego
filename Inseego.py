#!/usr/bin/env python3

import requests
import bcrypt
from bs4 import BeautifulSoup
import re
import json

class M3000:
    def __init__(self, address):
        self.salt_prefix = b'2a'
        self.salt_rounds = 10
        self.salt_len = 16
        self.url = 'http://' + address
        self.session = requests.Session()

    def get_soup(self, path):
        page = self.session.get(self.url + path)

        if not page.status_code == 200:
            raise Exception('bad response to login: %d' % (page.status_code))

        return(BeautifulSoup(page.content, "html.parser"))

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

    def restart(self):
        #token = self.get_soup('/restarting').find('input', { 'id':"gSecureToken"})['value']
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
        
