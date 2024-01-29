#!/usr/bin/env python3

from Inseego import M3000
#from Inseego import FX2000

m = Inseego.M3000('192.168.1.1')
#m = FX2000('192.168.1.1')

status = m.status()
print('connection: %(statusBarConnectionState)s' % status['statusData'])
print('network: %(statusBarNetwork)s' % status['statusData'])
print('technology: %(statusBarTechnology)s' % status['statusData'])
print('signal: %(statusBarSignalBars)s' % status['statusData'])
print()
