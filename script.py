#!/usr/bin/python

import json
import time
import threading
import requests
import random
# from progress.bar import Bar
from datetime import datetime

filename = "lista_urls.txt"

def create_json(nomeJson, logger):
    with open(nomeJson, 'w') as fp:
        json.dump(logger, fp)

def execute_url_list(casa, logger, nomeJson):
    try:
        start = time.time()
#        print(casa)
        result = requests.get(casa)
        end = time.time()
#        import ipdb; ipdb.set_trace()
        if not result.ok:
            log = {'url':casa,'status':result.status_code,'latency':end-start}
            logger['errors'].append(log)
#        else:
#            print('OK')
    except Exception as e:
        end = time.time()
        log = {'url':casa, 'status':str(e),'latency':end-start}
        logger['errors'].append(log)
        print('erro: %s' % casa)
    # create_json(nomeJson, logger)
    return logger

def threads(casas, logger, nomeJson):
    # bar = Bar('Loading', fill='@', suffix='%(percent)d%%',max= 1000)

    threads = [threading.Thread(target=execute_url_list,
              args=(casa,logger, nomeJson, )) for casa in casas]

    print("Start")
    for thread in threads:
        thread.start()
    #    bar.next()
    for thread in threads:
        thread.join()
    # bar.goto(1000)


def main():
#    while True:
        logger = {'errors':[]}
        nomeJson = "{}.json".format(datetime.now().strftime("%Y%m%dT%H%M"))
        with open(filename) as f:            
            casas = f.read().split()
            random.shuffle(casas)
            # casas = casas[1:2]
        start = 0
        end = 100
        while True:
            threads(casas[start:end], logger, nomeJson)
            print(end)
            if end > len(casas):
                break
            start = end
            end += 100
        print("Done!")
#        time.sleep(300)



if __name__ == '__main__':
    main()
