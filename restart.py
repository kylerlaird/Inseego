#!/usr/bin/env python3

import Inseego

password = input('password: ')

m = Inseego.M3000('192.168.1.1')
m.authenticate(password)
m.restart()
print('\nrestarting...')
