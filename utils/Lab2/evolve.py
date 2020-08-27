import requests
import time
import datetime


if __name__ == '__main__':
    while True:
        print(datetime.datetime.now())
        try:
            requests.get('http://3.131.111.217:46831/mserver/evolve?type=1')
            print('Successful')
        except Exception as e:
            print(e)
        print('Waiting for 330s...')
        time.sleep(330)
