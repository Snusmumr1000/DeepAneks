#!/usr/bin/env python3.6
import json, vk, markovify, time
from database import *
from random import randint

class DeepAnek:
    def __init__(self):
        try:
            with open("da_settings.json") as j:
                self.settings = json.loads(j.read())
            self._vk_api = vk.API(vk.Session(access_token=self.settings["vk_token"]))
        except Exception as e:
            with open("log", "a") as log:
                log.write(f'[{time.ctime()}] [DeepAneks] Init has failed. Exception {e.__class__} caught: retrying in 30 seconds...\n')
            time.sleep(30)

    def generate_anek(self):
        corpus = ""
        try:
            aneks = session.query(Anek)
            for anek in aneks:
                corpus += f"{anek.text}\n"
            model = markovify.Text(corpus)
            anek = ""
            for i in range(randint(2,6)):
                anek += model.make_short_sentence(500) + " "
            anek = anek.replace("–", "\n–")
            anek = anek.replace("- ", "\n- ")
            anek = anek.replace("—", "\n—")
            return anek
        except Exception as e:
            with open("log", "a") as log:
                log.write(f'[{time.ctime()}] [DeepAneks] Generation has failed. Exception {e.__class__} caught: retrying in 30 seconds...\n')
            time.sleep(30)

    def post(self):
        try:
            self._vk_api.wall.post(owner_id=self.settings["vk_id"], message=self.generate_anek(),
                                   from_group=1)
        except Exception as e:
            with open("log", "a") as log:
                log.write(f'[{time.ctime()}] [DeepAneks] Posting has failed. Exception {e.__class__} caught: retrying in 30 seconds...\n')
            time.sleep(30)


def main():
    posted = 0
    while not posted:
        DeepAnek().post()
        posted = 1


if __name__ == "__main__":
    main()
