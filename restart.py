#!/usr/bin/env python3

from Inseego import M3000 as AP
#from Inseego import FX2000 as AP

m = AP('192.168.1.1')

password = input('password: ')

m.authenticate(password)
m.restart()
print('\nrestarting...')
