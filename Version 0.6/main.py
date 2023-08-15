# -*- coding: utf-8 -*-
"""
    module to download,filter, paraphrase rewrite and summarise
    rss feed from multiple source
    version:0.6
"""
# from nlp import main
from server import ServeDirectoryWithHTTP
from urllib.request import urlopen
import schedule 
import time

from nlp import main

if __name__ == "__main__":
    try :
        # starting server 
        httpd, address = ServeDirectoryWithHTTP(directory="generated/")
        print("Address:", address)
        # running nlp program in first run
        main()

        # scheduling nlp program next run for every 24 hours
        schedule.every(24).hours.do(main)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt as e:
        httpd.shutdown()
        print("exiting program please wait...")
        exit()

