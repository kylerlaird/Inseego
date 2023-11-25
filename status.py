#!/usr/bin/env python3

import Inseego

m = Inseego.M3000('192.168.1.1')

status = m.status()
print('connection: %(statusBarConnectionState)s' % status['statusData'])
print('network: %(statusBarNetwork)s' % status['statusData'])
print('technology: %(statusBarTechnology)s' % status['statusData'])
print('signal: %(statusBarSignalBars)s' % status['statusData'])
print()
