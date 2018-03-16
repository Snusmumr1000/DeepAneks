#!/usr/bin/env python3.6
from time import sleep, ctime
from database import *
settings = [("mlj", 800), ("akb", 700), ("osa", 200)]
for setting in settings:
    total = 0
    aneks = session.query(Anek).filter(Anek.pub == setting[0], Anek.likes > setting[1])
    for e in aneks:
        best = Best(text=e.text,
                    likes=e.likes,
                    pub=e.pub
                    )
        if not session.query(Best).filter_by(text=best.text).all():
            session.add(best)
            total += 1
    with open("log", "a") as log:
        log.write(f"[{ctime()}] [Selector] A total of {total} aneks are added.\n")
'''
mlj
>800
'''

'''
osa
>200
'''

'''
akb
>700
'''