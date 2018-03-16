#!/usr/bin/env python3.6
import vk, json, time
from database import *


class Parser:
    def __init__(self):
        with open("settings.json", "r") as f:
            self.settings = json.loads(f.read())
        self._vk_token = self.settings["vk_token"]
        self.API = vk.API(vk.Session(access_token=self._vk_token))


    def filter_text(self, text):
        for z in self.settings["filter"]:
            if z in text:
                text = ""
                return text
        text = text.replace("<br>", "\n")
        text = text.replace("&gt;", ">")
        text = text.replace("&lt;", "<")
        return text


    def parse_pub(self, pub_id, pub_name="no name"):         
        offset = 0
        while True:
            try:
                posts = self.API.wall.get(owner_id=pub_id, count=100, offset=offset)['items']
                total = 0
                upd_total = 0
                for e in posts[1:]:
                    text = e["text"]
                    text = self.filter_text(text)
                    if text != "" and not ("attachment" in e):
                        likes = e["likes"]["count"]
                        res = f"{text} {likes}\n"
                        anek = Anek(
                            text=text,
                            likes=likes,
                            pub=pub_name
                            )
                        if not session.query(Anek).filter_by(text=anek.text).all():
                            session.add(anek)
                            total +=1
                        else:
                            for e in session.query(Anek).filter_by(text=anek.text).all():
                                old_likes = e.likes
                                if anek.likes > old_likes and e.pub == anek.pub:
                                    e.likes = anek.likes
                                    upd_total += 1
                                
                offset+=100
                time.sleep(1)
                session.commit()
                with open("verb_log", "a") as log:
                    log.write(f'[{time.ctime()}] [Parser] Stuff being parsed\n')
                if upd_total != 0:
                    with open("log", "a") as log:
                        log.write(f'[{time.ctime()}] [Parser] A total of {upd_total} aneks are updated\n')
                if total != 0:
                    with open("log", "a") as log:
                        log.write(f'[{time.ctime()}] [Parser] A total of {total} aneks are added\n')
                if len(posts) == 1 or offset>=200:
                    session.commit()
                    with open("log", "a") as log:
                        log.write(f'[{time.ctime()}] [Parser] Parsing is done\n')
                    return 1
            except Exception as e:
                with open("log", "a") as log:
                    log.write(f'[{time.ctime()}] [Parser] Exception {e.__class__} caught: retrying in 30 seconds..\n')
                time.sleep(30)


def main():
    for pub in Parser().settings["pubs"]:
        with open("log", "a") as log:
            log.write(f'[{time.ctime()}] {pub[1]} is being parsed..\n')
        Parser().parse_pub(pub[0], pub[1])


if __name__ == '__main__':
    main()
