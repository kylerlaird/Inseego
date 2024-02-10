#!/usr/bin/env python3

from Inseego import M3000 as AP
#from Inseego import FX2000 as AP

m = AP('192.168.1.1')

status = m.status()
print('connection: %(statusBarConnectionState)s' % status['statusData'])
print('network: %(statusBarNetwork)s' % status['statusData'])
print('technology: %(statusBarTechnology)s' % status['statusData'])
print('signal: %(statusBarSignalBars)s' % status['statusData'])
print()
