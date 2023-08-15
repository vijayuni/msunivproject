from server import ServeDirectoryWithHTTP
from urllib.request import urlopen
import schedule 
import time

from nlp import main

if __name__ == "__main__":
    try :
        httpd, address = ServeDirectoryWithHTTP(directory="generated/")
        print("Address:", address)
        main()

        schedule.every(24).hours.do(main)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt as e:
        httpd.shutdown()
        print("exiting program please wait...")
        exit()

