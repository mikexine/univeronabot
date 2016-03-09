#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import pickledb
from time import sleep

HEADERS = {
    'content-type': 'application/json'
    }

URL = 'http://188.166.145.27/api/univr/'

db = pickledb.load('db/univeronabot.pickledb', False)

mensa = requests.get(URL + 'mensa/', headers=HEADERS).json()
del mensa['last_update']
for key in mensa:
    print key
    if mensa[key]['calendario']['pranzo'] == 1:
        pranzo = True
    else:
        pranzo = False
    if mensa[key]['calendario']['cena'] == 1:
        cena = True
    else:
        cena = False

    if pranzo and cena:
        tmp = "oggi è aperta sia a pranzo che a cena"
    elif pranzo and not cena:
        tmp = "oggi è aperta solo a pranzo"
    elif cena and not pranzo:
        tmp = "oggi è aperta solo a cena"

    menupr = "-- PRANZO --\n-- PRIMO --\n%s\n-- SECONDO --\n%s\n--\
 CONTORNO --\n%s\n\n" % \
           (', '.join(mensa[key]['menu']['pranzo']['primo']),
            ', '.join(mensa[key]['menu']['pranzo']['secondo']),
            ', '.join(mensa[key]['menu']['pranzo']['contorno']))
    menuce = "-- CENA --\n-- PRIMO --\n%s\n-- SECONDO --\n%s\n--\
 CONTORNO --\n%s" % \
           (', '.join(mensa[key]['menu']['cena']['primo']),
            ', '.join(mensa[key]['menu']['cena']['secondo']),
            ', '.join(mensa[key]['menu']['cena']['contorno']))
    menu = menupr + menuce
    if not pranzo and not cena:
        text = '-- Mensa %s --\nIn %s.\nOggi la mensa è chiusa.\n' % \
                (mensa[key]['nome'].encode("utf-8"),
                 mensa[key]['indirizzo'].encode("utf-8"))
    else:
        text = '-- Mensa %s --\nIn %s, %s con orario: %s. \n' % \
                (mensa[key]['nome'].encode("utf-8"),
                 mensa[key]['indirizzo'].encode("utf-8"),
                 tmp,
                 mensa[key]['orari'].encode("utf-8"))
        text = text + menu.encode("utf-8")

    db.set(key, {'text': text, 'keyboard': [['/mensa'], ['/home']],
                 'coord': mensa[key]['coord']})

print 'sleeping'
sleep(2)

aulastudio = requests.get(URL + 'aulastudio/', headers=HEADERS).json()
for key in aulastudio:
    text = "-- %s --\nPosti: %s\nIndirizzo: %s\nOrari: %s.\n" % \
           (aulastudio[key]['nome'].encode("utf-8"),
            aulastudio[key]['posti'].encode("utf-8"),
            aulastudio[key]['indirizzo'].encode("utf-8"),
            aulastudio[key]['orario'].encode("utf-8"))
    db.set(key, {'text': text, 'keyboard': [['/aulastudio'], ['/home']],
                 'coord': aulastudio[key]['coord']})

print 'sleeping'
sleep(2)

biblioteca = requests.get(URL + 'biblioteca/', headers=HEADERS).json()
for key in biblioteca:
    text = "-- %s --\nIndirizzo: %s\nOrari: %s.\n" % \
           (biblioteca[key]['nome'].encode("utf-8"),
            biblioteca[key]['indirizzo'].encode("utf-8"),
            biblioteca[key]['orario'].encode("utf-8"))
    db.set(key, {'text': text, 'keyboard': [['/biblioteca'], ['/home']],
                 'coord': biblioteca[key]['coord']})

print 'sleeping'
sleep(2)


db.dump()
