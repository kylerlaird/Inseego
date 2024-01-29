#!/usr/bin/env python3

from Inseego import M3000
#from Inseego import FX2000

password = input('password: ')

m = M3000('192.168.1.1')
#m = FX2000('192.168.1.1')
m.authenticate(password)
m.restart()
print('\nrestarting...')
